import os
import io
import json
import wave
import uuid
import html
import secrets
import hashlib
from pathlib import Path
from urllib.parse import urlencode, quote
from datetime import datetime, timezone

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
