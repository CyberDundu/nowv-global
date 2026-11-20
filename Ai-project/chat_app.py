import os
import io
import json
import wave
import uuid
import html
import secrets
import hashlib

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError,
)
from pathlib import Path
from urllib.parse import urlencode, quote
from datetime import datetime, timezone, timedelta

import requests
import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from google import genai
from google.genai import types


# ==========================================
# PAGE CONFIGURATION — MUST COME FIRST
# ==========================================

st.set_page_config(
    page_title="NowV Live Chat & Video Messenger",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()


def get_secret(name: str) -> str:
    """Read Streamlit Cloud Secrets first, then local environment."""
    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        pass
    return os.getenv(name, "").strip()


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL").rstrip("/")
SUPABASE_KEY = get_secret("SUPABASE_KEY")
NOWV_APP_URL = get_secret("NOWV_APP_URL").rstrip("/")

if not GEMINI_API_KEY:
    st.error(
        "Gemini API key is missing. Add GEMINI_API_KEY to Streamlit "
        "Settings → Secrets or your local .env file."
    )
    st.stop()

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Supabase configuration is missing. Add SUPABASE_URL and "
        "SUPABASE_KEY to Streamlit Settings → Secrets or your local .env file."
    )
    st.stop()

# This key is used only by this server-side Streamlit application.
# Never place the Supabase secret key in browser-side JavaScript.
client = genai.Client(api_key=GEMINI_API_KEY)

LANGUAGES = {
    "Hausa": {"tts": "ha"},
    "English": {"tts": "en"},
    "Yoruba": {"tts": "en"},
    "Igbo": {"tts": "en"},
    "Mandarin Chinese": {"tts": "zh-CN"},
    "Nigerian Pidgin": {"tts": "en"},
    "Fulfulde": {"tts": "en"},
    "Kanuri": {"tts": "en"},
    "French": {"tts": "fr"},
    "Arabic": {"tts": "ar"},
    "Swahili": {"tts": "sw"},
    "Spanish": {"tts": "es"},
}

FAST_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
]

APP_DIR = Path(__file__).resolve().parent
MEDIA_BUCKET = "nowv-media"
MAX_MEDIA_BYTES = 50 * 1024 * 1024
MAX_MESSAGES = 100


# ==========================================
# SUPABASE REST HELPERS
# ==========================================

def sb_headers(content_type: str | None = "application/json") -> dict:
    # Supabase's new sb_secret_* keys are opaque API keys, not JWTs.
    # Send them in the apikey header only (not Authorization: Bearer).
    headers = {
        "apikey": SUPABASE_KEY,
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def sb_error(response: requests.Response, action: str) -> RuntimeError:
    detail = response.text[:1200]
    return RuntimeError(
        f"Supabase {action} failed ({response.status_code}): {detail}"
    )


def db_select(table: str, params: dict) -> list[dict]:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=sb_headers(),
        params=params,
        timeout=20,
    )
    if response.status_code != 200:
        raise sb_error(response, "read")
    return response.json()


def db_insert(table: str, payload: dict) -> dict:
    headers = sb_headers()
    headers["Prefer"] = "return=representation"
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=headers,
        json=payload,
        timeout=20,
    )
    if response.status_code not in (200, 201):
        raise sb_error(response, "insert")
    rows = response.json()
    return rows[0] if rows else {}


def db_update(table: str, filters: dict, payload: dict) -> None:
    headers = sb_headers()
    headers["Prefer"] = "return=minimal"
    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=headers,
        params=filters,
        json=payload,
        timeout=20,
    )
    if response.status_code not in (200, 204):
        raise sb_error(response, "update")



# ==========================================
# NOWV ACCOUNTS — PASSWORD SECURITY
# ==========================================

password_hasher = PasswordHasher()


def clean_nowv_id(value: str) -> str:
    value = str(value or "").upper().strip()
    return "".join(c for c in value if c.isalnum() or c == "-")[:40]


def register_nowv_user(
    display_name: str,
    preferred_lang: str,
    password: str,
) -> dict:
    display_name = str(display_name or "").strip()

    if len(display_name) < 2 or len(display_name) > 40:
        raise ValueError("Your display name must be 2–40 characters.")

    if preferred_lang not in LANGUAGES:
        raise ValueError("Please select a supported language.")

    if len(password) < 8:
        raise ValueError("Your password must contain at least 8 characters.")

    password_hash = password_hasher.hash(password)

    for _ in range(5):
        nowv_id = "NOWV-" + secrets.token_hex(4).upper()

        try:
            user = db_insert(
                "nowv_users",
                {
                    "nowv_id": nowv_id,
                    "display_name": display_name,
                    "preferred_lang": preferred_lang,
                    "password_hash": password_hash,
                },
            )
            return {
                "nowv_id": user.get("nowv_id", nowv_id),
                "display_name": user.get("display_name", display_name),
                "preferred_lang": user.get("preferred_lang", preferred_lang),
            }
        except RuntimeError as exc:
            error = str(exc).lower()
            if "23505" not in error and "duplicate key" not in error:
                raise

    raise RuntimeError("Could not generate a unique NowV ID. Please try again.")


class LoginLockedError(Exception):
    def __init__(self, minutes_remaining: int):
        self.minutes_remaining = minutes_remaining
        super().__init__(
            f"Too many failed attempts. Try again in approximately "
            f"{minutes_remaining} minute(s)."
        )


def authenticate_nowv_user(nowv_id: str, password: str) -> dict | None:
    nowv_id = clean_nowv_id(nowv_id)

    if not nowv_id or not password:
        return None

    locked, minutes_remaining = check_login_lockout(nowv_id)
    if locked:
        raise LoginLockedError(minutes_remaining)

    rows = db_select(
        "nowv_users",
        {
            "nowv_id": f"eq.{nowv_id}",
            "select": "nowv_id,display_name,preferred_lang,password_hash",
            "limit": "1",
        },
    )

    if not rows:
        record_failed_login(nowv_id)
        return None

    user = rows[0]
    stored_hash = str(user.get("password_hash") or "")

    if not stored_hash:
        record_failed_login(nowv_id)
        return None

    try:
        password_hasher.verify(stored_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        record_failed_login(nowv_id)
        return None

    if password_hasher.check_needs_rehash(stored_hash):
        db_update(
            "nowv_users",
            {"nowv_id": f"eq.{nowv_id}"},
            {"password_hash": password_hasher.hash(password)},
        )

    reset_login_attempts(nowv_id)

    return {
        "nowv_id": user["nowv_id"],
        "display_name": user["display_name"],
        "preferred_lang": user["preferred_lang"],
    }


# ==========================================
# LOGIN RATE LIMITING — SUPABASE
# ==========================================

MAX_LOGIN_FAILURES = 5
LOGIN_LOCKOUT_MINUTES = 15


def login_attempt_key(nowv_id: str) -> str:
    normalized = clean_nowv_id(nowv_id)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def check_login_lockout(nowv_id: str) -> tuple[bool, int]:
    key = login_attempt_key(nowv_id)

    rows = db_select(
        "nowv_login_attempts",
        {
            "attempt_key": f"eq.{key}",
            "select": "failed_attempts,locked_until",
            "limit": "1",
        },
    )

    if not rows:
        return False, 0

    row = rows[0]
    locked_until = row.get("locked_until")

    if not locked_until:
        return False, 0

    lock_time = datetime.fromisoformat(
        locked_until.replace("Z", "+00:00")
    )
    now = datetime.now(timezone.utc)

    if lock_time > now:
        remaining = max(
            1,
            int((lock_time - now).total_seconds() / 60) + 1,
        )
        return True, remaining

    reset_login_attempts(nowv_id)
    return False, 0
def record_failed_login(nowv_id: str) -> tuple[bool, int]:
    key = login_attempt_key(nowv_id)

    rows = db_select(
        "nowv_login_attempts",
        {
            "attempt_key": f"eq.{key}",
            "select": "failed_attempts",
            "limit": "1",
        },
    )

    failures = int(rows[0]["failed_attempts"]) + 1 if rows else 1

    locked_until = None
    if failures >= MAX_LOGIN_FAILURES:
        locked_until = (
            datetime.now(timezone.utc)
            + timedelta(minutes=LOGIN_LOCKOUT_MINUTES)
        ).isoformat()

    payload = {
        "attempt_key": key,
        "failed_attempts": failures,
        "locked_until": locked_until,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if rows:
        db_update(
            "nowv_login_attempts",
            {"attempt_key": f"eq.{key}"},
            {
                "failed_attempts": failures,
                "locked_until": locked_until,
                "updated_at": payload["updated_at"],
            },
        )
    else:
        db_insert("nowv_login_attempts", payload)

    return failures >= MAX_LOGIN_FAILURES, failures


def reset_login_attempts(nowv_id: str) -> None:
    key = login_attempt_key(nowv_id)

    rows = db_select(
        "nowv_login_attempts",
        {
            "attempt_key": f"eq.{key}",
            "select": "attempt_key",
            "limit": "1",
        },
    )

    if rows:
        db_update(
            "nowv_login_attempts",
            {"attempt_key": f"eq.{key}"},
            {
                "failed_attempts": 0,
                "locked_until": None,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )


# ==========================================
# ROOM MANAGEMENT — SUPABASE
# ==========================================

def clean_room_id(value: str) -> str:
    value = str(value or "").upper().strip()
    return "".join(c for c in value if c.isalnum() or c == "-")[:40]


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_room() -> tuple[str, str, str]:
    """Create a room and return room ID, owner token and guest token."""
    for _ in range(5):
        room_id = "NOWV-" + secrets.token_hex(3).upper()
        owner_token = secrets.token_urlsafe(32)
        guest_token = secrets.token_urlsafe(32)
        try:
            db_insert(
                "nowv_rooms",
                {
                    "room_id": room_id,
                    "owner_token_hash": hash_token(owner_token),
                    "guest_token_hash": hash_token(guest_token),
                    "language_a": None,
                    "language_b": None,
                },
            )
            return room_id, owner_token, guest_token
        except RuntimeError as exc:
            # Retry only for a room-code collision; surface other DB errors.
            if "23505" not in str(exc) and "duplicate key" not in str(exc).lower():
                raise
    raise RuntimeError("Could not generate a unique room code. Please retry.")


def verify_room_access(room_id: str, token: str, role: str) -> dict | None:
    if not room_id or not token or role not in ("owner", "guest"):
        return None
    rows = db_select(
        "nowv_rooms",
        {
            "room_id": f"eq.{room_id}",
            "select": "room_id,owner_token_hash,guest_token_hash,language_a,language_b,created_at",
            "limit": "1",
        },
    )
    if not rows:
        return None
    room = rows[0]
    column = "owner_token_hash" if role == "owner" else "guest_token_hash"
    expected = str(room.get(column) or "")
    if not expected or not secrets.compare_digest(expected, hash_token(token)):
        return None
    return room


def get_room(room_id: str) -> dict | None:
    rows = db_select(
        "nowv_rooms",
        {
            "room_id": f"eq.{room_id}",
            "select": "room_id,language_a,language_b,created_at",
            "limit": "1",
        },
    )
    return rows[0] if rows else None


def save_participant_language(room_id: str, side: str, language: str) -> None:
    column = "language_a" if side == "A" else "language_b"
    db_update(
        "nowv_rooms",
        {"room_id": f"eq.{room_id}"},
        {column: language},
    )


# ==========================================
# DIRECT MESSAGES — PRIVATE CONVERSATIONS
# ==========================================

def search_nowv_users(search_id: str, current_nowv_id: str) -> list[dict]:
    """Find registered users by exact NowV ID without exposing private fields."""
    target_id = clean_nowv_id(search_id)
    current_id = clean_nowv_id(current_nowv_id)

    if not target_id or target_id == current_id:
        return []

    rows = db_select(
        "nowv_users",
        {
            "nowv_id": f"eq.{target_id}",
            "select": "nowv_id,display_name,preferred_lang",
            "limit": "1",
        },
    )
    return rows


def get_or_create_dm_thread(current_nowv_id: str, other_nowv_id: str) -> dict:
    """Return the one permanent private thread shared by two users."""
    current_id = clean_nowv_id(current_nowv_id)
    other_id = clean_nowv_id(other_nowv_id)

    if not current_id or not other_id:
        raise ValueError("Both NowV IDs are required.")

    if current_id == other_id:
        raise ValueError("You cannot start a conversation with yourself.")

    # Verify both accounts exist.
    users = db_select(
        "nowv_users",
        {
            "nowv_id": f"in.({current_id},{other_id})",
            "select": "nowv_id",
            "limit": "2",
        },
    )
    found_ids = {row.get("nowv_id") for row in users}
    if current_id not in found_ids or other_id not in found_ids:
        raise ValueError("One or both NowV accounts could not be found.")

    user_a, user_b = sorted((current_id, other_id))

    existing = db_select(
        "nowv_dm_threads",
        {
            "user_a": f"eq.{user_a}",
            "user_b": f"eq.{user_b}",
            "select": "*",
            "limit": "1",
        },
    )
    if existing:
        return existing[0]

    thread_id = "NOWVDM-" + uuid.uuid4().hex[:16].upper()

    try:
        return db_insert(
            "nowv_dm_threads",
            {
                "thread_id": thread_id,
                "user_a": user_a,
                "user_b": user_b,
                "last_message": "",
            },
        )
    except Exception:
        # A simultaneous request may have created the same user pair.
        existing = db_select(
            "nowv_dm_threads",
            {
                "user_a": f"eq.{user_a}",
                "user_b": f"eq.{user_b}",
                "select": "*",
                "limit": "1",
            },
        )
        if existing:
            return existing[0]
        raise


def fetch_dm_messages(thread_id: str, current_nowv_id: str) -> list[dict]:
    """Fetch messages only when the current account belongs to the thread."""
    current_id = clean_nowv_id(current_nowv_id)
    safe_thread_id = str(thread_id or "").strip()

    if not current_id or not safe_thread_id:
        raise ValueError("A valid account and conversation are required.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{safe_thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )

    if not threads:
        raise ValueError("Conversation not found.")

    thread = threads[0]
    if current_id not in (thread.get("user_a"), thread.get("user_b")):
        raise PermissionError("You do not have access to this conversation.")

    return db_select(
        "nowv_dm_messages",
        {
            "thread_id": f"eq.{safe_thread_id}",
            "select": "*",
            "order": "id.asc",
            "limit": str(MAX_MESSAGES),
        },
    )


def send_dm_message(
    thread_id: str,
    current_user: dict,
    message_text: str,
    source_lang: str,
    reply_to_message_id: int | None = None,
) -> dict:
    """Translate and save a text message in an authorized private thread."""
    current_id = clean_nowv_id(str(current_user.get("nowv_id") or ""))
    text = str(message_text or "").strip()

    if not current_id:
        raise ValueError("Please sign in before sending a message.")

    if not text:
        raise ValueError("Message cannot be empty.")

    if len(text) > 10000:
        raise ValueError("Message is too long. Maximum length is 10,000 characters.")

    if source_lang not in LANGUAGES:
        raise ValueError("Please select a supported language.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )

    if not threads:
        raise ValueError("Conversation not found.")

    thread = threads[0]
    if current_id not in (thread.get("user_a"), thread.get("user_b")):
        raise PermissionError("You do not have access to this conversation.")

    if reply_to_message_id is not None:
        try:
            reply_id = int(reply_to_message_id)
        except (TypeError, ValueError):
            raise ValueError("Invalid reply message.")
        reply_rows = db_select(
            "nowv_dm_messages",
            {
                "id": f"eq.{reply_id}",
                "thread_id": f"eq.{thread_id}",
                "select": "id,deleted_at",
                "limit": "1",
            },
        )
        if not reply_rows or reply_rows[0].get("deleted_at"):
            raise ValueError("The message you are replying to is unavailable.")
    else:
        reply_id = None

    receiver_id = (
        thread["user_b"] if current_id == thread["user_a"]
        else thread["user_a"]
    )

    receiver_rows = db_select(
        "nowv_users",
        {
            "nowv_id": f"eq.{receiver_id}",
            "select": "nowv_id,preferred_lang",
            "limit": "1",
        },
    )

    if not receiver_rows:
        raise ValueError("The other participant's account could not be found.")

    receiver_lang = receiver_rows[0].get("preferred_lang") or "English"

    translated = translate_chat_text(text, source_lang, receiver_lang)

    saved_message = db_insert(
        "nowv_dm_messages",
        {
            "thread_id": thread_id,
            "sender_nowv_id": current_id,
            "original_text": text,
            "translated_text": translated,
            "source_lang": source_lang,
            "target_lang": receiver_lang,
            "kind": "Text",
            "reply_to_message_id": reply_id,
        },
    )

    db_update(
        "nowv_dm_threads",
        {"thread_id": f"eq.{thread_id}"},
        {
            "last_message": text[:200],
            "last_message_sender_id": current_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    return saved_message



def send_dm_voice_message(
    thread_id: str,
    current_user: dict,
    audio_bytes: bytes,
    mime_type: str,
    source_lang: str,
    reply_to_message_id: int | None = None,
) -> dict:
    """Save a voice note with transcription and recipient-language translation."""
    current_id = clean_nowv_id(str(current_user.get("nowv_id") or ""))
    if not current_id or not audio_bytes:
        raise ValueError("A signed-in account and a voice recording are required.")
    if len(audio_bytes) > MAX_MEDIA_BYTES:
        raise ValueError("Voice recording exceeds the 50 MB upload limit.")
    if source_lang not in LANGUAGES:
        raise ValueError("Please select a supported language.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )
    if not threads:
        raise ValueError("Conversation not found.")

    thread = threads[0]
    if current_id not in (thread.get("user_a"), thread.get("user_b")):
        raise PermissionError("You cannot access this conversation.")

    receiver_id = (
        thread["user_b"] if current_id == thread["user_a"]
        else thread["user_a"]
    )
    receiver_rows = db_select(
        "nowv_users",
        {
            "nowv_id": f"eq.{receiver_id}",
            "select": "nowv_id,preferred_lang",
            "limit": "1",
        },
    )
    if not receiver_rows:
        raise ValueError("The recipient account could not be found.")

    receiver_lang = receiver_rows[0].get("preferred_lang") or "English"

    reply_id = None
    if reply_to_message_id is not None:
        reply_id = int(reply_to_message_id)
        reply_rows = db_select(
            "nowv_dm_messages",
            {
                "id": f"eq.{reply_id}",
                "thread_id": f"eq.{thread_id}",
                "select": "id,deleted_at",
                "limit": "1",
            },
        )
        if not reply_rows or reply_rows[0].get("deleted_at"):
            raise ValueError("The reply message is unavailable.")

    transcript, translated = translate_media_or_audio(
        audio_bytes, mime_type, source_lang, receiver_lang
    )
    if not transcript and not translated:
        raise ValueError("No speech could be recognized. Please try again.")

    suffix = {
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/webm": "webm",
        "audio/mp4": "m4a",
        "audio/mpeg": "mp3",
        "audio/ogg": "ogg",
    }.get(mime_type, "wav")

    media_path = upload_media(
        f"dm/{thread_id}", audio_bytes, mime_type, suffix
    )

    speech_path = None
    if translated:
        translated_audio = generate_speech_bytes(translated, receiver_lang)
        if translated_audio:
            try:
                speech_path = upload_media(
                    f"dm/{thread_id}",
                    translated_audio,
                    "audio/mpeg",
                    "mp3",
                )
            except Exception:
                speech_path = None

    saved = db_insert(
        "nowv_dm_messages",
        {
            "thread_id": thread_id,
            "sender_nowv_id": current_id,
            "original_text": transcript,
            "translated_text": translated,
            "source_lang": source_lang,
            "target_lang": receiver_lang,
            "kind": "Voice",
            "media_path": media_path,
            "media_mime": mime_type,
            "speech_path": speech_path,
            "reply_to_message_id": reply_id,
        },
    )

    db_update(
        "nowv_dm_threads",
        {"thread_id": f"eq.{thread_id}"},
        {
            "last_message": ("🎙️ " + (transcript or "Voice message"))[:200],
            "last_message_sender_id": current_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return saved


def mark_dm_thread_read(thread_id: str, current_nowv_id: str) -> None:
    current_id = clean_nowv_id(current_nowv_id)
    safe_thread_id = str(thread_id or "").strip()

    if not current_id or not safe_thread_id:
        raise ValueError("Invalid conversation or user ID.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{safe_thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )

    if not threads:
        raise ValueError("Conversation not found.")

    thread = threads[0]
    if current_id == thread["user_a"]:
        read_column = "user_a_last_read_at"
    elif current_id == thread["user_b"]:
        read_column = "user_b_last_read_at"
    else:
        raise PermissionError("You are not a member of this conversation.")

    now = datetime.now(timezone.utc).isoformat()

    # Mark every incoming message as read.
    db_update(
        "nowv_dm_messages",
        {
            "thread_id": f"eq.{safe_thread_id}",
            "sender_nowv_id": f"neq.{current_id}",
            "read_at": "is.null",
        },
        {"read_at": now},
    )

    # Preserve the existing conversation-level unread indicator.
    db_update(
        "nowv_dm_threads",
        {"thread_id": f"eq.{safe_thread_id}"},
        {read_column: now},
    )


def edit_dm_message(
    thread_id: str,
    current_nowv_id: str,
    message_id: int,
    new_text: str,
) -> None:
    current_id = clean_nowv_id(current_nowv_id)
    text = str(new_text or "").strip()

    if not current_id or not text:
        raise ValueError("Message and account are required.")
    if len(text) > 10000:
        raise ValueError("Message is too long.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )
    if not threads or current_id not in (
        threads[0].get("user_a"), threads[0].get("user_b")
    ):
        raise PermissionError("You cannot access this conversation.")

    rows = db_select(
        "nowv_dm_messages",
        {
            "id": f"eq.{int(message_id)}",
            "thread_id": f"eq.{thread_id}",
            "select": "id,sender_nowv_id,source_lang,target_lang,deleted_at",
            "limit": "1",
        },
    )
    if not rows or rows[0].get("deleted_at"):
        raise ValueError("Message not found or already deleted.")
    message = rows[0]

    if message.get("sender_nowv_id") != current_id:
        raise PermissionError("You can only edit your own messages.")

    source_lang = message.get("source_lang") or "English"
    target_lang = message.get("target_lang") or "English"
    translated = translate_chat_text(text, source_lang, target_lang)

    db_update(
        "nowv_dm_messages",
        {
            "id": f"eq.{int(message_id)}",
            "thread_id": f"eq.{thread_id}",
        },
        {
            "original_text": text,
            "translated_text": translated,
            "edited_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def delete_dm_message(
    thread_id: str,
    current_nowv_id: str,
    message_id: int,
) -> None:
    current_id = clean_nowv_id(current_nowv_id)
    if not current_id:
        raise ValueError("Please sign in.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "thread_id": f"eq.{thread_id}",
            "select": "thread_id,user_a,user_b",
            "limit": "1",
        },
    )
    if not threads or current_id not in (
        threads[0].get("user_a"), threads[0].get("user_b")
    ):
        raise PermissionError("You cannot access this conversation.")

    rows = db_select(
        "nowv_dm_messages",
        {
            "id": f"eq.{int(message_id)}",
            "thread_id": f"eq.{thread_id}",
            "select": "id,sender_nowv_id,deleted_at",
            "limit": "1",
        },
    )
    if not rows or rows[0].get("deleted_at"):
        raise ValueError("Message not found or already deleted.")
    if rows[0].get("sender_nowv_id") != current_id:
        raise PermissionError("You can only delete your own messages.")

    db_update(
        "nowv_dm_messages",
        {
            "id": f"eq.{int(message_id)}",
            "thread_id": f"eq.{thread_id}",
        },
        {
            "deleted_at": datetime.now(timezone.utc).isoformat(),
            "deleted_by": current_id,
        },
    )


def fetch_dm_threads(current_nowv_id: str) -> list[dict]:
    """Fetch every private conversation belonging to the signed-in user."""
    current_id = clean_nowv_id(current_nowv_id)
    if not current_id:
        raise ValueError("Please sign in to view your conversations.")

    threads = db_select(
        "nowv_dm_threads",
        {
            "or": f"(user_a.eq.{current_id},user_b.eq.{current_id})",
            "select": "thread_id,user_a,user_b,last_message,updated_at,last_message_sender_id,user_a_last_read_at,user_b_last_read_at",
            "order": "updated_at.desc",
            "limit": "100",
        },
    )

    other_ids = {
        thread["user_b"] if thread["user_a"] == current_id else thread["user_a"]
        for thread in threads
    }

    if not other_ids:
        return []

    users = db_select(
        "nowv_users",
        {
            "nowv_id": f"in.({','.join(sorted(other_ids))})",
            "select": "nowv_id,display_name,preferred_lang",
        },
    )

    users_by_id = {user["nowv_id"]: user for user in users}

    for thread in threads:
        other_id = (
            thread["user_b"]
            if thread["user_a"] == current_id
            else thread["user_a"]
        )
        thread["other_user"] = users_by_id.get(other_id, {
            "nowv_id": other_id,
            "display_name": other_id,
            "preferred_lang": "English",
        })

    return threads


# ==========================================
# SUPABASE STORAGE — AUDIO AND VIDEO
# ==========================================

def upload_media(room_id: str, media_bytes: bytes, mime_type: str, suffix: str) -> str:
    if not media_bytes:
        raise ValueError("The selected media file is empty.")
    if len(media_bytes) > MAX_MEDIA_BYTES:
        raise ValueError("Media file exceeds the 50 MB NowV upload limit.")

    object_path = f"{room_id}/{uuid.uuid4().hex}.{suffix}"
    safe_path = quote(object_path, safe="/")
    headers = sb_headers(mime_type)
    headers["x-upsert"] = "false"

    response = requests.post(
        f"{SUPABASE_URL}/storage/v1/object/{MEDIA_BUCKET}/{safe_path}",
        headers=headers,
        data=media_bytes,
        timeout=90,
    )
    if response.status_code not in (200, 201):
        raise sb_error(response, "media upload")
    return object_path


def download_media(object_path: str | None) -> bytes | None:
    if not object_path:
        return None

    cache = st.session_state.setdefault("_nowv_media_cache", {})
    if object_path in cache:
        return cache[object_path]

    safe_path = quote(object_path, safe="/")
    response = requests.get(
        f"{SUPABASE_URL}/storage/v1/object/{MEDIA_BUCKET}/{safe_path}",
        headers=sb_headers(None),
        timeout=45,
    )
    if response.status_code != 200:
        raise sb_error(response, "media download")

    data = response.content
    cache[object_path] = data
    # Keep the session cache bounded.
    if len(cache) > 12:
        oldest_key = next(iter(cache))
        if oldest_key != object_path:
            cache.pop(oldest_key, None)
    return data


# ==========================================
# MESSAGE STORAGE — SUPABASE
# ==========================================

def fetch_messages(room_id: str) -> list[dict]:
    return db_select(
        "nowv_messages",
        {
            "room_id": f"eq.{room_id}",
            "select": "*",
            "order": "id.asc",
            "limit": str(MAX_MESSAGES),
        },
    )


def insert_message(
    room_id: str,
    sender_side: str,
    source_lang: str,
    target_lang: str,
    original_text: str,
    translated_text: str,
    kind: str = "Text",
    media_path: str | None = None,
    speech_path: str | None = None,
    media_mime: str | None = None,
) -> None:
    db_insert(
        "nowv_messages",
        {
            "room_id": room_id,
            "sender": sender_side,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "original_text": original_text,
            "translated_text": translated_text,
            "kind": kind,
            "media_path": media_path,
            "speech_path": speech_path,
            "media_mime": media_mime,
        },
    )


# ==========================================
# GEMINI TRANSLATION FUNCTIONS
# ==========================================

def compress_wav_bytes(wav_bytes: bytes) -> bytes:
    """Convert WAV audio to mono 16 kHz where possible."""
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
            rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frames = wav_file.readframes(wav_file.getnframes())

        if sample_width != 2:
            return wav_bytes

        import numpy as np
        audio = np.frombuffer(frames, dtype=np.int16)
        if channels > 1:
            audio = audio[::channels]

        step = max(1, round(rate / 16000))
        reduced = audio[::step]
        output = io.BytesIO()
        with wave.open(output, "wb") as wav_out:
            wav_out.setnchannels(1)
            wav_out.setsampwidth(2)
            wav_out.setframerate(max(1, rate // step))
            wav_out.writeframes(reduced.tobytes())
        return output.getvalue()
    except Exception:
        return wav_bytes


def translate_chat_text(text: str, sender_lang: str, receiver_lang: str) -> str:
    if sender_lang == receiver_lang:
        return text

    prompt = (
        "You are NowV Global's professional trade interpreter. "
        f"Translate this conversational message from {sender_lang} into "
        f"{receiver_lang}. Preserve prices, quantities, product specifications, "
        "names, measurements and tone. Return only the translation, without "
        f"explanations:\n\n{text}"
    )
    last_error = ""
    for model_name in FAST_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2),
            )
            result = (response.text or "").strip()
            if result:
                return result
            raise RuntimeError("Gemini returned an empty translation.")
        except Exception as exc:
            last_error = str(exc)
    raise RuntimeError(f"Text translation failed: {last_error}")


def translate_media_or_audio(
    media_bytes: bytes,
    mime_type: str,
    sender_lang: str,
    receiver_lang: str,
) -> tuple[str, str]:
    prompt = (
        "You are NowV Global's professional trade interpreter. "
        f"Transcribe the speech in {sender_lang}, then translate it naturally "
        f"into {receiver_lang}. Preserve names, prices, quantities and product "
        "details. Return valid JSON with exactly two keys: "
        '"transcription" and "translation".'
    )

    if mime_type == "audio/wav":
        media_bytes = compress_wav_bytes(media_bytes)

    media_part = types.Part.from_bytes(data=media_bytes, mime_type=mime_type)
    last_error = ""
    for model_name in FAST_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[media_part, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            result = json.loads(response.text or "{}")
            transcript = str(result.get("transcription", "")).strip()
            translation = str(result.get("translation", "")).strip()
            if not transcript and not translation:
                raise RuntimeError("Gemini returned no transcription or translation.")
            return transcript, translation
        except Exception as exc:
            last_error = str(exc)
    raise RuntimeError(f"Media translation failed: {last_error}")


def generate_speech_bytes(text: str, language: str) -> bytes | None:
    if not text:
        return None
    tts_code = LANGUAGES.get(language, {}).get("tts")
    if not tts_code:
        return None
    try:
        speech = gTTS(text=text[:4500], lang=tts_code)
        buffer = io.BytesIO()
        speech.write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:
        # TTS is an enhancement; the translated text remains available.
        return None


# ==========================================
# VISUAL DESIGN
# ==========================================

st.markdown(
    """
    <style>
    .stApp { background: #0b141a; color: #e9edef; }
    .wa-header {
        background: linear-gradient(135deg, #075e54 0%, #128c7e 100%);
        padding: 1rem 1.3rem; border-radius: 14px;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,.25);
    }
    .wa-bubble-me {
        background: #005c4b; color: #e9edef; padding: .75rem 1rem;
        border-radius: 14px 14px 2px 14px; margin: .45rem 0 .45rem 18%;
        box-shadow: 0 1px 3px rgba(0,0,0,.2); overflow-wrap: anywhere;
    }
    .wa-bubble-them {
        background: #202c33; color: #e9edef; padding: .75rem 1rem;
        border-radius: 14px 14px 14px 2px; margin: .45rem 18% .45rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,.2); overflow-wrap: anywhere;
    }
    .wa-meta { font-size: .75rem; color: #aebac1; margin-bottom: .4rem; }
    .wa-trans {
        margin-top: .4rem; padding-top: .4rem;
        border-top: 1px solid rgba(255,255,255,.12);
        color: #8bd5f5; font-weight: 600; overflow-wrap: anywhere;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# LOGO / HEADER
# ==========================================

logo_candidates = [
    APP_DIR / "logo.png",
    APP_DIR / "logo.jpg",
    APP_DIR / "logo.jpeg",
]
logo_file = next((item for item in logo_candidates if item.exists()), None)

if logo_file:
    encoded_logo = __import__("base64").b64encode(logo_file.read_bytes()).decode()
    logo_tag = (
        f'<img src="data:image/png;base64,{encoded_logo}" '
        'style="height:38px;width:auto;object-fit:contain;">'
    )
else:
    logo_tag = '<span style="font-size:1.8rem;">💬</span>'

st.markdown(
    f"""
    <div class="wa-header">
      <div style="display:flex;align-items:center;gap:.8rem;">
        {logo_tag}
        <div>
          <div style="color:#fff;font-weight:800;font-size:1.2rem;">
            NowV Live Bilingual Messenger
          </div>
          <div style="color:#d1fae5;font-size:.8rem;">
            ● Cloud-connected • Text, Voice & Video Translation
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# NOWV APP MODE — ROOM OR DIRECT MESSAGES
# ==========================================

query_room = clean_room_id(st.query_params.get("room", ""))

if not query_room or st.session_state.get("nowv_app_mode") == "Direct Messages":
    st.markdown("## Welcome to NowV")
    st.caption("Choose how you want to communicate.")

    app_mode = st.radio(
        "Messenger",
        ["Room Messenger", "Direct Messages"],
        horizontal=True,
        key="nowv_app_mode",
    )

    if app_mode == "Direct Messages":
        st.markdown("### Your NowV Account")

        current_user = st.session_state.get("nowv_user")

        if current_user:
            if st.session_state.pop("nowv_account_created", False):
                st.success("Your NowV account was created successfully.")

            st.success(
                f"Signed in as {current_user['display_name']} "
                f"({current_user['nowv_id']})"
            )
            st.caption(
                f"Default language: {current_user['preferred_lang']}"
            )

            if st.button("Log Out", use_container_width=True):
                st.session_state.pop("nowv_user", None)
                st.rerun()

            st.markdown("### Find People")
            with st.form("nowv_find_user_form", clear_on_submit=True):
                search_id = st.text_input(
                    "Search by NowV ID",
                    placeholder="NOWV-XXXXXXXX",
                )
                search_submit = st.form_submit_button(
                    "Find User",
                    use_container_width=True,
                )

            if search_submit:
                try:
                    matches = search_nowv_users(
                        search_id,
                        current_user["nowv_id"],
                    )
                    if matches:
                        st.session_state["nowv_found_user"] = matches[0]
                    else:
                        st.session_state.pop("nowv_found_user", None)
                        st.warning("No account found with that NowV ID.")
                except Exception as exc:
                    st.error(f"User search failed: {exc}")

            found_user = st.session_state.get("nowv_found_user")
            if found_user:
                st.markdown("#### Search Result")
                st.write(f"**{found_user['display_name']}**")
                st.caption(
                    f"{found_user['nowv_id']} · "
                    f"Language: {found_user['preferred_lang']}"
                )
                if st.button(
                    "Message This User",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        thread = get_or_create_dm_thread(
                            current_user["nowv_id"],
                            found_user["nowv_id"],
                        )
                        st.session_state["nowv_active_dm"] = thread["thread_id"]
                        st.success("Private conversation opened.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not open conversation: {exc}")

            st.divider()

            @st.fragment(run_every=3)
            def render_dm_conversations(user_id):
                st.markdown("### Your Conversations")

                try:
                    threads = fetch_dm_threads(user_id)
                except Exception as exc:
                    st.error(f"Could not load conversations: {exc}")
                    return

                if not threads:
                    st.info(
                        "No private conversations yet. Find someone by "
                        "their NowV ID to start a conversation."
                    )
                    return

                for dm_thread in threads:
                    other_user = dm_thread["other_user"]
                    thread_id = dm_thread["thread_id"]
                    is_active = (
                        st.session_state.get("nowv_active_dm") == thread_id
                    )

                    preview = (
                        dm_thread.get("last_message") or "Start a conversation"
                    ).replace("\\n", " ").strip()

                    if len(preview) > 65:
                        preview = preview[:62] + "..."

                    updated = dm_thread.get("updated_at", "")
                    try:
                        stamp = datetime.fromisoformat(
                            updated.replace("Z", "+00:00")
                        ).astimezone().strftime("%d %b · %H:%M")
                    except (ValueError, TypeError, AttributeError):
                        stamp = ""

                    current_id = clean_nowv_id(user_id)
                    read_field = (
                        "user_a_last_read_at"
                        if current_id == dm_thread.get("user_a")
                        else "user_b_last_read_at"
                    )
                    last_read = dm_thread.get(read_field)
                    unread = False

                    if (
                        dm_thread.get("last_message_sender_id")
                        and dm_thread.get("last_message_sender_id") != current_id
                        and updated
                    ):
                        try:
                            message_time = datetime.fromisoformat(
                                updated.replace("Z", "+00:00")
                            )
                            read_time = (
                                datetime.fromisoformat(
                                    last_read.replace("Z", "+00:00")
                                )
                                if last_read else None
                            )
                            if message_time.tzinfo is None:
                                message_time = message_time.replace(
                                    tzinfo=timezone.utc
                                )
                            if read_time and read_time.tzinfo is None:
                                read_time = read_time.replace(
                                    tzinfo=timezone.utc
                                )
                            unread = (
                                read_time is None or message_time > read_time
                            )
                        except (ValueError, TypeError, AttributeError):
                            unread = False

                    label = (
                        f"{'✓ ' if is_active else ''}"
                        f"{'🔵 ' if unread else ''}"
                        f"{other_user['display_name']} · "
                        f"{other_user['nowv_id']}\n"
                        f"{preview}  ·  {stamp}"
                    )

                    if st.button(
                        label,
                        key=f"open_dm_{thread_id}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                    ):
                        st.session_state["nowv_active_dm"] = thread_id
                        st.rerun()

            render_dm_conversations(current_user["nowv_id"])

            try:
                dm_threads = fetch_dm_threads(current_user["nowv_id"])
            except Exception as exc:
                dm_threads = []
                st.error(f"Could not load active conversation: {exc}")

            if dm_threads:
                active_thread_id = st.session_state.get("nowv_active_dm")
                active_thread = next(
                    (
                        item for item in dm_threads
                        if item["thread_id"] == active_thread_id
                    ),
                    None,
                )

                if active_thread:
                    current_id = clean_nowv_id(current_user["nowv_id"])
                    read_field = (
                        "user_a_last_read_at"
                        if current_id == active_thread.get("user_a")
                        else "user_b_last_read_at"
                    )
                    last_read = active_thread.get(read_field)
                    last_sender = active_thread.get("last_message_sender_id")
                    updated = active_thread.get("updated_at")

                    if last_sender and last_sender != current_id and updated:
                        try:
                            message_time = datetime.fromisoformat(
                                updated.replace("Z", "+00:00")
                            )
                            read_time = (
                                datetime.fromisoformat(
                                    last_read.replace("Z", "+00:00")
                                )
                                if last_read else None
                            )
                            if message_time.tzinfo is None:
                                message_time = message_time.replace(
                                    tzinfo=timezone.utc
                                )
                            if read_time and read_time.tzinfo is None:
                                read_time = read_time.replace(
                                    tzinfo=timezone.utc
                                )

                            if read_time is None or message_time > read_time:
                                mark_dm_thread_read(
                                    active_thread_id,
                                    current_user["nowv_id"],
                                )
                        except (ValueError, TypeError, AttributeError) as exc:
                            st.warning(f"Could not update read status: {exc}")

                    other = active_thread["other_user"]
                    st.divider()
                    st.markdown(f"### Chat with {other['display_name']}")
                    st.caption(
                        f"{other['nowv_id']} · "
                        f"Your language: {current_user['preferred_lang']} · "
                        f"Their language: {other['preferred_lang']}"
                    )

                    st.text_input(
                        "Search messages in this conversation",
                        key=f"dm_search_{active_thread_id}",
                        placeholder="Search message text...",
                    )

                    @st.fragment(run_every=2)
                    def render_dm_messages(thread_id, user_id, other_name):
                        try:
                            messages = fetch_dm_messages(thread_id, user_id)
                        except Exception as exc:
                            st.error(f"Could not load messages: {exc}")
                            return

                        search_term = st.session_state.get(
                            f"dm_search_{thread_id}", ""
                        ).strip().casefold()

                        messages_by_id = {
                            str(message.get("id")): message for message in messages
                        }

                        visible_messages = []
                        for message in messages:
                            searchable = (
                                str(message.get("original_text") or "")
                                + " "
                                + str(message.get("translated_text") or "")
                            ).casefold()
                            if not search_term or search_term in searchable:
                                visible_messages.append(message)

                        if not visible_messages:
                            st.caption(
                                "No messages match your search."
                                if search_term else "No messages yet. Start the conversation."
                            )

                        for dm_message in visible_messages:
                            message_id = dm_message.get("id")
                            is_mine = dm_message.get("sender_nowv_id") == user_id
                            sender_label = "You" if is_mine else other_name
                            deleted = bool(dm_message.get("deleted_at"))

                            created = dm_message.get("created_at")
                            try:
                                timestamp = datetime.fromisoformat(
                                    str(created).replace("Z", "+00:00")
                                ).astimezone().strftime("%b %d, %I:%M %p")
                            except (ValueError, TypeError):
                                timestamp = ""

                            with st.chat_message("user" if is_mine else "assistant"):
                                st.caption(
                                    f"{sender_label} · {timestamp}"
                                    + (" · Edited" if dm_message.get("edited_at") else "")
                                )

                                reply_id = dm_message.get("reply_to_message_id")
                                if reply_id is not None:
                                    replied = messages_by_id.get(str(reply_id))
                                    if replied:
                                        reply_preview = (
                                            "Message deleted"
                                            if replied.get("deleted_at")
                                            else str(replied.get("original_text") or "")[:160]
                                        )
                                        st.caption(f"↪ Replying to: {reply_preview}")

                                if deleted:
                                    st.caption("This message was deleted.")
                                else:
                                    message_kind = str(
                                        dm_message.get("kind") or "Text"
                                    ).lower()
                                    original = dm_message.get("original_text") or ""
                                    translated = dm_message.get("translated_text") or ""

                                    is_voice_message = (
                                        message_kind == "voice"
                                        or bool(dm_message.get("media_path"))
                                    )
                                    if is_voice_message:
                                        st.caption("🎙️ Voice message")
                                        media_path = dm_message.get("media_path")
                                        media_mime = (
                                            dm_message.get("media_mime") or "audio/wav"
                                        )

                                        if media_path:
                                            try:
                                                voice_bytes = download_media(media_path)
                                                if voice_bytes:
                                                    st.audio(
                                                        voice_bytes,
                                                        format=media_mime,
                                                    )
                                            except Exception as audio_exc:
                                                st.caption(
                                                    f"Original audio unavailable: {audio_exc}"
                                                )

                                        if original:
                                            st.caption(
                                                f"Transcription ({dm_message.get('source_lang', 'original')}):"
                                            )
                                            st.write(original)

                                        if translated and translated != original:
                                            st.caption(
                                                f"Translation ({dm_message.get('target_lang', 'translated')}):"
                                            )
                                            st.write(translated)

                                        speech_path = dm_message.get("speech_path")
                                        if speech_path:
                                            try:
                                                speech_bytes = download_media(speech_path)
                                                if speech_bytes:
                                                    st.caption("🔊 Translated audio")
                                                    st.audio(
                                                        speech_bytes,
                                                        format="audio/mpeg",
                                                    )
                                            except Exception:
                                                st.caption(
                                                    "Translated audio is temporarily unavailable."
                                                )
                                    else:
                                        st.write(original)
                                        if translated and translated != original:
                                            st.caption(
                                                f"Translation ({dm_message.get('target_lang', 'translated')}):"
                                            )
                                            st.write(translated)
                                            if not is_mine:
                                                t_col1, t_col2 = st.columns([1, 1.3])
                                                with t_col1:
                                                    if st.button(
                                                        "🔊 Listen",
                                                        key=f"dm_tts_{thread_id}_{message_id}",
                                                    ):
                                                        tts_bytes = generate_speech_bytes(
                                                            translated,
                                                            dm_message.get("target_lang", "English"),
                                                        )
                                                        if tts_bytes:
                                                            st.audio(
                                                                tts_bytes,
                                                                format="audio/mpeg",
                                                            )
                                                with t_col2:
                                                    if st.button(
                                                        "🔍 Verify Meaning",
                                                        key=f"dm_verify_{thread_id}_{message_id}",
                                                    ):
                                                        try:
                                                            verified = translate_chat_text(
                                                                translated,
                                                                dm_message.get("target_lang", "English"),
                                                                dm_message.get("source_lang", "English"),
                                                            )
                                                            st.caption(
                                                                f"Back-translation: {verified}"
                                                            )
                                                        except Exception as verify_exc:
                                                            st.caption(
                                                                f"Verification unavailable: {verify_exc}"
                                                            )

                                if is_mine:
                                    st.caption(
                                        "✓✓ Read" if dm_message.get("read_at") else "✓ Sent"
                                    )

                                if not deleted:
                                    if st.button(
                                        "Reply",
                                        key=f"dm_reply_{thread_id}_{message_id}",
                                    ):
                                        st.session_state["nowv_dm_reply"] = {
                                            "thread_id": thread_id,
                                            "message_id": message_id,
                                            "preview": str(
                                                dm_message.get("original_text") or ""
                                            )[:100],
                                        }
                                        st.rerun()

                                    if is_mine:
                                        with st.expander("Edit message"):
                                            with st.form(
                                                f"dm_edit_form_{thread_id}_{message_id}"
                                            ):
                                                edited_text = st.text_area(
                                                    "Updated message",
                                                    value=dm_message.get("original_text", ""),
                                                    max_chars=10000,
                                                    key=f"dm_edit_text_{thread_id}_{message_id}",
                                                )
                                                edit_submit = st.form_submit_button("Save edit")

                                            if edit_submit:
                                                try:
                                                    edit_dm_message(
                                                        thread_id,
                                                        user_id,
                                                        message_id,
                                                        edited_text,
                                                    )
                                                    st.success("Message updated.")
                                                    st.rerun()
                                                except Exception as exc:
                                                    st.error(f"Could not edit message: {exc}")

                                        if st.button(
                                            "Delete message",
                                            key=f"dm_delete_{thread_id}_{message_id}",
                                        ):
                                            try:
                                                delete_dm_message(
                                                    thread_id, user_id, message_id
                                                )
                                                st.success("Message deleted.")
                                                st.rerun()
                                            except Exception as exc:
                                                st.error(f"Could not delete message: {exc}")


                    render_dm_messages(
                        active_thread_id,
                        current_user["nowv_id"],
                        other["display_name"],
                    )

                    reply_state = st.session_state.get("nowv_dm_reply")
                    if reply_state and reply_state.get("thread_id") == active_thread_id:
                        st.info(f"Replying to: {reply_state.get('preview', '')}")
                        if st.button("Cancel reply", key=f"dm_cancel_reply_{active_thread_id}"):
                            st.session_state.pop("nowv_dm_reply", None)
                            st.rerun()
                    else:
                        reply_state = None

                    with st.form(
                        f"dm_message_form_{active_thread_id}",
                        clear_on_submit=True,
                    ):
                        message_text = st.text_area(
                            "Message",
                            placeholder="Type your message...",
                            max_chars=10000,
                        )
                        source_lang = st.selectbox(
                            "Your message language",
                            list(LANGUAGES.keys()),
                            index=(
                                list(LANGUAGES.keys()).index(current_user["preferred_lang"])
                                if current_user["preferred_lang"] in LANGUAGES else 0
                            ),
                            key=f"dm_language_{active_thread_id}",
                        )
                        send_submit = st.form_submit_button(
                            "Send Message",
                            type="primary",
                            use_container_width=True,
                        )

                    if send_submit:
                        try:
                            send_dm_message(
                                active_thread_id,
                                current_user,
                                message_text,
                                source_lang,
                                reply_state.get("message_id") if reply_state else None,
                            )
                            st.session_state.pop("nowv_dm_reply", None)
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Message could not be sent: {exc}")
                    with st.expander("🎙️ Record a voice note"):
                        st.caption(
                            "Record in your selected language. NowV will transcribe "
                            "and translate it for the recipient."
                        )
                        voice_input_version_key = (
                            f"dm_voice_input_version_{active_thread_id}"
                        )
                        if voice_input_version_key not in st.session_state:
                            st.session_state[voice_input_version_key] = 0

                        audio_file = st.audio_input(
                            "Record a voice note",
                            key=(
                                f"dm_voice_input_{active_thread_id}_"
                                f"{st.session_state[voice_input_version_key]}"
                            ),
                        )

                        if audio_file is not None:
                            audio_data = audio_file.getvalue()
                            audio_mime = audio_file.type or "audio/wav"
                            audio_hash = hashlib.sha256(audio_data).hexdigest()
                            sent_hash_key = f"dm_voice_sent_{active_thread_id}"

                            if audio_data:
                                st.audio(audio_data, format=audio_mime)

                                if st.button(
                                    "Send voice note",
                                    key=f"dm_voice_send_{active_thread_id}",
                                    type="primary",
                                ):
                                    if st.session_state.get(sent_hash_key) == audio_hash:
                                        st.info("This recording has already been sent.")
                                    else:
                                        try:
                                            voice_source_lang = st.session_state.get(
                                                f"dm_language_{active_thread_id}",
                                                current_user.get("preferred_lang", "English"),
                                            )
                                            send_dm_voice_message(
                                                active_thread_id,
                                                current_user,
                                                audio_data,
                                                audio_mime,
                                                voice_source_lang,
                                                reply_state.get("message_id")
                                                if reply_state else None,
                                            )
                                            st.session_state[sent_hash_key] = audio_hash
                                            st.session_state[voice_input_version_key] += 1
                                            st.session_state.pop("nowv_dm_reply", None)
                                            st.success("Voice note sent.")
                                            st.rerun()
                                        except Exception as voice_exc:
                                            st.error(
                                                f"Voice note could not be sent: {voice_exc}"
                                            )


            else:
                st.info(
                    "No private conversations yet. Find someone by their "
                    "NowV ID to start a conversation."
                )

        else:
            login_tab, register_tab = st.tabs(
                ["Log In", "Create Account"]
            )

            with login_tab:
                with st.form("nowv_login_form", clear_on_submit=True):
                    login_id = st.text_input(
                        "NowV ID",
                        placeholder="NOWV-XXXXXXXX",
                    )
                    login_password = st.text_input(
                        "Password",
                        type="password",
                    )
                    login_submit = st.form_submit_button(
                        "Log In",
                        type="primary",
                        use_container_width=True,
                    )

                if login_submit:
                    try:
                        user = authenticate_nowv_user(
                            login_id,
                            login_password,
                        )
                        if user:
                            st.session_state["nowv_user"] = user
                            st.rerun()
                        else:
                            st.error("Incorrect NowV ID or password.")
                    except LoginLockedError as exc:
                        st.error(str(exc))
                    except Exception as exc:
                        st.error(f"Login failed: {exc}")

            with register_tab:
                with st.form("nowv_register_form", clear_on_submit=True):
                    display_name = st.text_input(
                        "Your display name",
                        max_chars=40,
                    )
                    preferred_lang = st.selectbox(
                        "Your default language",
                        list(LANGUAGES.keys()),
                        index=list(LANGUAGES.keys()).index("English"),
                    )
                    new_password = st.text_input(
                        "Create password",
                        type="password",
                    )
                    confirm_password = st.text_input(
                        "Confirm password",
                        type="password",
                    )
                    register_submit = st.form_submit_button(
                        "Create My NowV Account",
                        type="primary",
                        use_container_width=True,
                    )

                if register_submit:
                    if new_password != confirm_password:
                        st.error("Your passwords do not match.")
                    else:
                        try:
                            user = register_nowv_user(
                                display_name,
                                preferred_lang,
                                new_password,
                            )
                            st.session_state["nowv_user"] = user
                            st.session_state["nowv_account_created"] = True
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                        except Exception as exc:
                            st.error(f"Account creation failed: {exc}")

        st.stop()


# ==========================================
# PARTICIPANT ACCESS / PRIVATE ROOM TOKENS
# ==========================================

query_room = clean_room_id(st.query_params.get("room", ""))
query_owner_token = str(st.query_params.get("owner", "") or "")
query_guest_token = str(st.query_params.get("invite", "") or "")

if "room_id" not in st.session_state:
    if query_room:
        try:
            room_meta = None
            participant_side = None
            if query_owner_token:
                room_meta = verify_room_access(query_room, query_owner_token, "owner")
                participant_side = "A"
            elif query_guest_token:
                room_meta = verify_room_access(query_room, query_guest_token, "guest")
                participant_side = "B"

            if not room_meta:
                st.error(
                    "This room link is invalid or expired. Ask the room creator "
                    "to send a fresh private invitation."
                )
                st.stop()

            st.session_state.room_id = query_room
            st.session_state.participant_side = participant_side
            st.session_state.room_meta = room_meta
            if participant_side == "A":
                st.session_state.owner_token = query_owner_token
                st.session_state.guest_invite_token = None
            else:
                st.session_state.owner_token = None
                st.session_state.guest_invite_token = query_guest_token
        except Exception as exc:
            st.error(f"Could not open the room: {exc}")
            st.stop()
    else:
        try:
            new_room, owner_token, guest_token = create_room()
            st.session_state.room_id = new_room
            st.session_state.participant_side = "A"
            st.session_state.owner_token = owner_token
            st.session_state.guest_invite_token = guest_token
            st.session_state.room_meta = get_room(new_room)
            st.query_params["room"] = new_room
            st.query_params["owner"] = owner_token
        except Exception as exc:
            st.error(f"Could not create a chat room: {exc}")
            st.stop()

elif query_room and query_room != st.session_state.room_id:
    try:
        room_meta = None
        participant_side = None
        if query_owner_token:
            room_meta = verify_room_access(query_room, query_owner_token, "owner")
            participant_side = "A"
        elif query_guest_token:
            room_meta = verify_room_access(query_room, query_guest_token, "guest")
            participant_side = "B"

        if not room_meta:
            st.error("Invalid private room invitation.")
            st.stop()

        st.session_state.room_id = query_room
        st.session_state.participant_side = participant_side
        st.session_state.room_meta = room_meta
        st.session_state.owner_token = query_owner_token if participant_side == "A" else None
        st.session_state.guest_invite_token = query_guest_token if participant_side == "B" else None
        st.session_state.pop("_nowv_media_cache", None)
    except Exception as exc:
        st.error(f"Could not join that room: {exc}")
        st.stop()

room_id = st.session_state.room_id
side = st.session_state.participant_side
other_side = "B" if side == "A" else "A"
role_label = "Room Creator" if side == "A" else "Invited Partner"


# ==========================================
# ROOM INVITATION INTERFACE
# ==========================================

with st.expander("🔗 Conversation Room & Private Invitation", expanded=True):
    st.markdown(f"**Room code:** `{room_id}`")
    st.caption(f"You are {role_label} (Participant {side}).")

    public_app_url = (NOWV_APP_URL or "https" + "://nowv-ai-live-chat.streamlit.app").strip().rstrip("/")

    if side == "A":
        guest_token = st.session_state.get("guest_invite_token")
        if public_app_url and guest_token:
            invite_url = (
                public_app_url
                + "/?"
                + urlencode({"room": room_id, "invite": guest_token})
            )
            st.text_input(
                "Private invitation link for your partner",
                value=invite_url,
            )
            st.caption("Share this private link only with your intended conversation partner.")
        else:
            st.info("Enter the deployed app URL above to create your private invitation link.")
    else:
        st.success("You joined the room using a private invitation.")

    st.divider()
    st.markdown("**Join another room**")
    join_code = st.text_input("Room code", placeholder="NOWV-XXXXXX", key="nowv_join_code")
    join_token = st.text_input(
        "Private invitation token",
        type="password",
        key="nowv_join_token",
    )
    if st.button("Join Room", use_container_width=True):
        new_room_id = clean_room_id(join_code)
        try:
            new_meta = verify_room_access(new_room_id, join_token, "guest")
            if not new_meta:
                st.error("Room not found or private invitation token is invalid.")
            else:
                st.query_params["room"] = new_room_id
                st.query_params["invite"] = join_token
                if "owner" in st.query_params:
                    del st.query_params["owner"]
                st.rerun()
        except Exception as exc:
            st.error(f"Could not join room: {exc}")

    if st.button("➕ Create New Room", use_container_width=True):
        try:
            new_room_id, new_owner_token, new_guest_token = create_room()
            st.session_state.room_id = new_room_id
            st.session_state.participant_side = "A"
            st.session_state.owner_token = new_owner_token
            st.session_state.guest_invite_token = new_guest_token
            st.session_state.room_meta = get_room(new_room_id)
            st.session_state.pop("_nowv_media_cache", None)
            st.query_params["room"] = new_room_id
            st.query_params["owner"] = new_owner_token
            if "invite" in st.query_params:
                del st.query_params["invite"]
            st.rerun()
        except Exception as exc:
            st.error(f"Could not create a new room: {exc}")


# ==========================================
# INDEPENDENT LANGUAGE SETTINGS
# ==========================================

try:
    room_meta = get_room(room_id)
except Exception as exc:
    st.error(f"Could not load room settings: {exc}")
    st.stop()

if not room_meta:
    st.error("This room no longer exists.")
    st.stop()

language_column = "language_a" if side == "A" else "language_b"
saved_language = room_meta.get(language_column)
language_options = list(LANGUAGES.keys())
default_language = "English" if side == "A" else "Mandarin Chinese"
if saved_language not in language_options:
    saved_language = default_language

language_state_key = f"nowv_language_{room_id}_{side}"
if language_state_key not in st.session_state:
    st.session_state[language_state_key] = saved_language

st.markdown("### 🌍 Your Language Settings")
st.caption("Choose your own language. Your partner chooses their language independently.")

my_lang = st.selectbox(
    "Your Language (Speak & Read)",
    language_options,
    key=language_state_key,
)

if room_meta.get(language_column) != my_lang:
    try:
        save_participant_language(room_id, side, my_lang)
        room_meta[language_column] = my_lang
    except Exception as exc:
        st.error(f"Could not save your language: {exc}")
        st.stop()

their_lang = room_meta.get("language_b" if side == "A" else "language_a")

if not their_lang:
    st.warning(
        "Waiting for your partner to join and choose their language. "
        "Once they select it, press Refresh Conversation."
    )
    if st.button("Refresh Room", use_container_width=True):
        st.rerun()
    st.stop()

st.info(f"Your language: **{my_lang}**  |  Partner's language: **{their_lang}**")


# ==========================================
# CHAT HISTORY — CLOUD REFRESH
# ==========================================

st.markdown("### 💬 Conversation")


@st.fragment(run_every=1.5)
def render_chat_history():
    try:
        messages = fetch_messages(room_id)
    except Exception as exc:
        st.error(f"Could not load messages: {exc}")
        return

    with st.container(height=430):
        if not messages:
            st.info(
                "👋 Your private NowV room is ready. Send a text, voice note "
                "or video message to begin."
            )
            return

        for message in messages:
            sender = str(message.get("sender", ""))
            # New rows store A/B. Keep compatibility with earlier buyer/seller labels.
            is_me = sender == side or (sender == "You" and side == "A")
            sender_label = "You" if is_me else "Partner"
            bubble_class = "wa-bubble-me" if is_me else "wa-bubble-them"

            source_lang = html.escape(str(message.get("source_lang", "")))
            target_lang = html.escape(str(message.get("target_lang", "")))
            original = html.escape(str(message.get("original_text", ""))).replace("\n", "<br>")
            translated = html.escape(str(message.get("translated_text", ""))).replace("\n", "<br>")
            created_at = str(message.get("created_at", ""))
            try:
                stamp = datetime.fromisoformat(created_at.replace("Z", "+00:00")).astimezone().strftime("%H:%M")
            except Exception:
                stamp = ""
            kind = html.escape(str(message.get("kind") or "Text"))

            st.markdown(
                f"""
                <div class="{bubble_class}">
                  <div class="wa-meta">
                    {sender_label} • {stamp} • {source_lang} → {target_lang} ({kind})
                  </div>
                  <div>{original}</div>
                  <div class="wa-trans">🔊 {target_lang}: {translated}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            media_path = message.get("media_path")
            speech_path = message.get("speech_path")
            if media_path:
                try:
                    media_bytes = download_media(media_path)
                    if media_bytes:
                        mime = message.get("media_mime") or ""
                        if mime.startswith("video/"):
                            st.video(media_bytes)
                        elif mime.startswith("audio/"):
                            st.audio(media_bytes, format=mime)
                except Exception as exc:
                    st.warning(f"Media could not be loaded: {exc}")

            if speech_path:
                try:
                    speech_bytes = download_media(speech_path)
                    if speech_bytes:
                        st.audio(speech_bytes, format="audio/mp3")
                except Exception as exc:
                    st.warning(f"Translated audio could not be loaded: {exc}")


render_chat_history()


# ==========================================
# MESSAGE INPUT
# ==========================================

st.markdown("### ✉️ Send a Message")

tab_text, tab_audio, tab_video = st.tabs([
    "⌨️ Text Message",
    "🎙️ Voice Note",
    "🎥 Video Message",
])


def save_outgoing_message(
    original_text: str,
    translated_text: str,
    kind: str,
    media_bytes: bytes | None = None,
    media_mime: str | None = None,
    media_suffix: str | None = None,
) -> None:
    media_path = None
    speech_path = None

    speech_bytes = generate_speech_bytes(translated_text, their_lang)
    try:
        if media_bytes and media_mime and media_suffix:
            media_path = upload_media(room_id, media_bytes, media_mime, media_suffix)
        if speech_bytes:
            speech_path = upload_media(room_id, speech_bytes, "audio/mpeg", "mp3")

        insert_message(
            room_id=room_id,
            sender_side=side,
            source_lang=my_lang,
            target_lang=their_lang,
            original_text=original_text,
            translated_text=translated_text,
            kind=kind,
            media_path=media_path,
            speech_path=speech_path,
            media_mime=media_mime,
        )
    except Exception:
        # The app does not silently report a successful send if cloud storage fails.
        raise


with tab_text:
    with st.form("nowv_text_message_form", clear_on_submit=True):
        text_message = st.text_area(
            f"Message in {my_lang}",
            placeholder=f"Write in {my_lang}; your partner receives {their_lang}...",
            height=100,
        )
        text_submit = st.form_submit_button(
            "Send Message ➤",
            type="primary",
            use_container_width=True,
        )

    if text_submit:
        if not text_message.strip():
            st.warning("Type a message before sending.")
        else:
            with st.spinner(f"Translating {my_lang} → {their_lang}..."):
                try:
                    translated_text = translate_chat_text(
                        text_message.strip(),
                        my_lang,
                        their_lang,
                    )
                    save_outgoing_message(
                        text_message.strip(),
                        translated_text,
                        "Text",
                    )
                    st.success("Message sent.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Message could not be sent: {exc}")


with tab_audio:
    voice_note = st.audio_input(
        f"Record in {my_lang} — translates to {their_lang}",
        key="nowv_voice_input",
    )
    if voice_note is not None:
        raw_audio = voice_note.getvalue()
        clip_hash = hashlib.sha256(raw_audio).hexdigest()
        if st.session_state.get("last_nowv_audio_hash") != clip_hash:
            if len(raw_audio) > MAX_MEDIA_BYTES:
                st.error("This voice note is larger than the 50 MB upload limit.")
            else:
                with st.spinner(f"Transcribing and translating {my_lang} → {their_lang}..."):
                    try:
                        transcript, translated = translate_media_or_audio(
                            raw_audio,
                            "audio/wav",
                            my_lang,
                            their_lang,
                        )
                        save_outgoing_message(
                            f"🎙️ {transcript}",
                            translated,
                            "Voice Note",
                            media_bytes=raw_audio,
                            media_mime="audio/wav",
                            media_suffix="wav",
                        )
                        st.session_state["last_nowv_audio_hash"] = clip_hash
                        st.success("Voice note sent.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Voice note could not be sent: {exc}")


with tab_video:
    st.caption(
        f"Upload a short video clip in {my_lang}. NowV transcribes its speech "
        f"and translates it into {their_lang}."
    )
    video_file = st.file_uploader(
        "Upload Video Clip",
        type=["mp4", "mov", "webm"],
        key="nowv_video_upload",
    )
    if video_file is not None:
        video_bytes = video_file.getvalue()
        video_hash = hashlib.sha256(video_bytes).hexdigest()
        if len(video_bytes) > MAX_MEDIA_BYTES:
            st.error("This video exceeds the 50 MB upload limit.")
        elif st.session_state.get("last_nowv_video_hash") != video_hash:
            if st.button("🎥 Send & Translate Video", type="primary", use_container_width=True):
                with st.spinner(f"Transcribing and translating video: {my_lang} → {their_lang}..."):
                    try:
                        video_mime = video_file.type or "video/mp4"
                        spoken_video, translated_video = translate_media_or_audio(
                            video_bytes,
                            video_mime,
                            my_lang,
                            their_lang,
                        )
                        save_outgoing_message(
                            f"🎥 {spoken_video}",
                            translated_video,
                            "Video Message",
                            media_bytes=video_bytes,
                            media_mime=video_mime,
                            media_suffix=Path(video_file.name).suffix.lstrip(".") or "mp4",
                        )
                        st.session_state["last_nowv_video_hash"] = video_hash
                        st.success("Video message sent.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Video could not be sent: {exc}")


# ==========================================
# FOOTER / MANUAL REFRESH
# ==========================================

st.divider()
if st.button("🔄 Refresh Conversation", use_container_width=True):
    st.rerun()

st.caption("NowV Live Messenger • Private two-person conversations • Cloud-synced by Supabase")
