import os
import secrets
from pathlib import Path
from urllib.parse import urlencode
import io
import wave
import json
import base64
from datetime import datetime
import numpy as np
import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# Read API key from local environment or Streamlit Cloud Secrets.
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error(
        "Gemini API key is missing. "
        "Configure GEMINI_API_KEY in your environment or Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

LANGUAGES = {
    "Hausa": "ha",
    "English": "en",
    "Yoruba": "yo",
    "Igbo": None,
    "Mandarin Chinese": "zh-CN",
    "Nigerian Pidgin": None,
    "Fulfulde": None,
    "Kanuri": None,
    "French": "fr",
    "Arabic": "ar",
    "Swahili": "sw",
    "Spanish": "es",
}

FAST_MODELS = ["gemini-3.5-flash-lite", "gemini-2.5-flash"]

def compress_wav_bytes(wav_bytes):
    """Shrinks WAV audio to lightweight 16kHz mono for fast upload."""
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
            rate = wf.getframerate()
            channels = wf.getnchannels()
            frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)
        if channels > 1:
            audio = audio[::channels]
        step = max(1, rate // 16000)
        small_audio = audio[::step]
        out = io.BytesIO()
        with wave.open(out, "wb") as wf_out:
            wf_out.setnchannels(1)
            wf_out.setsampwidth(2)
            wf_out.setframerate(rate // step)
            wf_out.writeframes(small_audio.tobytes())
        return out.getvalue()
    except Exception:
        return wav_bytes

def translate_media_or_audio(media_bytes, mime_type, sender_lang, receiver_lang):
    """Transcribes spoken audio or video in sender_lang and translates into receiver_lang."""
    prompt = (
        f"You are a real-time native interpreter fluent in Hausa, Yoruba, Igbo, Fulfulde, Kanuri, "
        f"Nigerian Pidgin, English, Mandarin Chinese, French, Arabic, Swahili, and Spanish.\n"
        f"Listen carefully to the spoken words in this {mime_type} clip in {sender_lang}.\n"
        f"1. Transcribe accurately what was said in {sender_lang}.\n"
        f"2. Translate it naturally into {receiver_lang} as if in a live WhatsApp conversation.\n"
        f"Return ONLY valid JSON with exact keys 'transcription' and 'translation'."
    )
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2,
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
                config=config,
            )
            data = json.loads(response.text)
            return data.get("transcription", "").strip(), data.get("translation", "").strip()
        except Exception as e:
            last_error = str(e)
            continue
    raise RuntimeError(f"Media translation failed: {last_error}")

def translate_chat_text(text, sender_lang, receiver_lang):
    """Translates chat text naturally from sender_lang into receiver_lang."""
    if sender_lang == receiver_lang:
        return text
    prompt = (
        f"You are a real-time native interpreter fluent in Hausa, Yoruba, Igbo, Fulfulde, Kanuri, "
        f"Nigerian Pidgin, English, Mandarin Chinese, French, Arabic, Swahili, and Spanish.\n"
        f"Translate this conversational message from {sender_lang} into {receiver_lang} naturally.\n"
        f"Return ONLY the translated message:\n\n{text}"
    )
    config = types.GenerateContentConfig(temperature=0.2)
    last_error = ""

    for model_name in FAST_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            return response.text.strip()
        except Exception as e:
            last_error = str(e)
            continue
    raise RuntimeError(f"Text translation failed: {last_error}")

def generate_speech_bytes(text, speak_code):
    if not speak_code or not text:
        return None
    tts = gTTS(text=text[:500], lang=speak_code)
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer.read()

def get_logo_b64(path):
    with open(path, "rb") as img_f:
        return base64.b64encode(img_f.read()).decode()

# --- PAGE CONFIG & WHATSAPP-STYLE NOWV THEME ---
st.set_page_config(page_title="NowV Live Chat & Video Messenger", page_icon="💬", layout="centered")

logo_file = next((f for f in ["logo.png", "logo.jpg", "logo.jpeg"] if os.path.exists(f)), None)
logo_tag = (
    f'<img src="data:image/png;base64,{get_logo_b64(logo_file)}" style="height: 38px; width: auto; object-fit: contain;">'
    if logo_file else '<span style="font-size: 1.8rem;">💬</span>'
)

st.markdown(f"""
<style>
.wa-header {{
    background: linear-gradient(135deg, #075e54 0%, #128c7e 100%);
    padding: 1rem 1.3rem;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}}
.wa-bubble-me {{
    background-color: #005c4b;
    color: #e9edef;
    padding: 0.75rem 1rem;
    border-radius: 14px 14px 2px 14px;
    margin: 0.45rem 0 0.45rem 18%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.wa-bubble-them {{
    background-color: #202c33;
    color: #e9edef;
    padding: 0.75rem 1rem;
    border-radius: 14px 14px 14px 2px;
    margin: 0.45rem 18% 0.45rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.wa-meta {{
    font-size: 0.75rem;
    color: #8696a0;
    margin-bottom: 0.25rem;
}}
.wa-trans {{
    margin-top: 0.4rem;
    padding-top: 0.4rem;
    border-top: 1px solid rgba(255,255,255,0.12);
    color: #53bdeb;
    font-weight: 600;
}}
</style>
<div class="wa-header">
    <div style="display:flex; align-items:center; gap:0.8rem;">
        {logo_tag}
        <div>
            <div style="color:#ffffff; font-weight:800; font-size:1.2rem;">NowV Live Bilingual Messenger</div>
            <div style="color:#d1fae5; font-size:0.8rem;">● Online • Auto-Translating Text, Voice & Video</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



# ==========================================
# NOWV SHARED CHAT ROOMS — PROTOTYPE STORAGE
# ==========================================

ROOMS_DIR = Path(__file__).resolve().parent / "chat_rooms"
ROOMS_DIR.mkdir(parents=True, exist_ok=True)


def clean_room_id(value):
    value = str(value or "").upper().strip()
    return "".join(
        char for char in value
        if char.isalnum() or char == "-"
    )[:40]


def create_room_id():
    return "NOWV-" + secrets.token_hex(3).upper()


def room_file(room_id):
    return ROOMS_DIR / f"{clean_room_id(room_id)}.json"


def load_room_messages(room_id):
    file_path = room_file(room_id)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            messages = json.load(file)

        for message in messages:
            for media_key in ("audio_bytes", "video_bytes"):
                encoded = message.get(media_key)
                if encoded:
                    message[media_key] = base64.b64decode(encoded)

        return messages

    except (OSError, ValueError, TypeError):
        return []


def save_room_messages(room_id, messages):
    file_path = room_file(room_id)
    serializable = []

    for message in messages:
        item = dict(message)

        for media_key in ("audio_bytes", "video_bytes"):
            media = item.get(media_key)
            if isinstance(media, bytes):
                item[media_key] = base64.b64encode(media).decode("ascii")

        serializable.append(item)

    temporary_file = file_path.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(serializable, file, ensure_ascii=False)

    temporary_file.replace(file_path)


def add_message(message):
    st.session_state.wa_messages.append(message)
    save_room_messages(
        st.session_state.room_id,
        st.session_state.wa_messages,
    )


requested_room = clean_room_id(st.query_params.get("room", ""))

if "room_id" not in st.session_state:
    st.session_state.room_id = requested_room or create_room_id()
elif requested_room and requested_room != st.session_state.room_id:
    st.session_state.room_id = requested_room
    st.session_state.wa_messages = load_room_messages(requested_room)

if "wa_messages" not in st.session_state:
    st.session_state.wa_messages = load_room_messages(
        st.session_state.room_id
    )




# ==========================================
# ROOM CONTROLS AND INVITATION LINK
# ==========================================

with st.expander("🔗 Conversation Room & Invitation", expanded=True):
    st.markdown(f"**Your room code:** `{st.session_state.room_id}`")

    public_app_url = st.text_input(
        "Public NowV chat app URL",
        value=os.getenv("NOWV_APP_URL", ""),
        placeholder="https://your-app-name.streamlit.app",
        help="Enter your deployed Streamlit app address.",
    ).strip()

    if public_app_url:
        invite_url = (
            public_app_url.rstrip("/")
            + "/?"
            + urlencode({"room": st.session_state.room_id})
        )
        st.text_input("Share this invitation link", value=invite_url)
        st.caption("Send this link to the person you want to chat with.")
    else:
        st.caption(
            "Enter your deployed app URL above to create a shareable link."
        )

    join_col, create_col = st.columns(2)

    with join_col:
        join_code = st.text_input(
            "Enter another room code",
            placeholder="NOWV-XXXXXX",
            key="nowv_join_code",
        )
        if st.button("Join Room", use_container_width=True):
            new_room = clean_room_id(join_code)
            if new_room:
                st.query_params["room"] = new_room
                st.rerun()
            else:
                st.warning("Enter a valid room code.")

    with create_col:
        if st.button("Create New Room", use_container_width=True):
            new_room = create_room_id()
            st.query_params["room"] = new_room
            st.rerun()


lang_names = list(LANGUAGES.keys())

# --- TWO-SIDED INDEPENDENT LANGUAGE SETTINGS ---
col_you, col_them = st.columns(2)
with col_you:
    st.markdown("**🧑🏾 Your Settings (Side A)**")
    my_lang = st.selectbox("Your Language (Speak & Hear)", lang_names, index=1, key="my_lang")  # Default English
with col_them:
    st.markdown("**🌍 Listener / Partner Settings (Side B)**")
    their_lang = st.selectbox("Listener's Language (Speak & Hear)", lang_names, index=0, key="their_lang")  # Default Hausa

ctrl1, ctrl2 = st.columns([3, 1])
with ctrl1:
    active_sender = st.radio(
        "Active Sender:",
        [f"🧑🏾 You ({my_lang} → {their_lang})", f"🌍 Partner ({their_lang} → {my_lang})"],
        horizontal=True,
    )
with ctrl2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.wa_messages = []
        save_room_messages(st.session_state.room_id, [])
        st.rerun()

# --- WHATSAPP CHAT FEED ---
chat_box = st.container(height=360)
with chat_box:
    if not st.session_state.wa_messages:
        st.info("👋 Start chatting below! Pick **Text**, **Voice Note**, or **Video Clip**—every message translates automatically into the listener's chosen language.")
    for idx, m in enumerate(st.session_state.wa_messages):
        is_me = m["sender"] == "You"
        bubble_class = "wa-bubble-me" if is_me else "wa-bubble-them"
        st.markdown(f"""
        <div class="{bubble_class}">
            <div class="wa-meta">{m['sender']} • {m['time']} • {m['from_lang']} → {m['to_lang']} ({m['kind']})</div>
            <div>{m['original']}</div>
            <div class="wa-trans">🔊 {m['to_lang']}: {m['translated']}</div>
        </div>
        """, unsafe_allow_html=True)

        if m.get("video_bytes"):
            st.video(m["video_bytes"])
        if m.get("audio_bytes"):
            is_newest = idx == len(st.session_state.wa_messages) - 1
            st.audio(m["audio_bytes"], format="audio/mp3", autoplay=is_newest)

# --- SENDER INPUT BAR: TEXT, AUDIO, OR VIDEO ---
is_me_sending = active_sender.startswith("🧑🏾 You")
from_lang = my_lang if is_me_sending else their_lang
to_lang = their_lang if is_me_sending else my_lang
sender_name = "You" if is_me_sending else "Partner"

mode_tab_text, mode_tab_audio, mode_tab_video = st.tabs([
    "⌨️ Text Message",
    "🎙️ Voice Note (Audio)",
    "🎥 Video Message",
])

with mode_tab_text:
    msg_text = st.text_input(
        f"Message as {sender_name} ({from_lang})...",
        key="wa_text_in",
        placeholder=f"Type in {from_lang} — listener receives {to_lang}...",
    )
    if st.button("Send Message ➤", type="primary", use_container_width=True):
        if msg_text.strip():
            with st.spinner(f"Translating to {to_lang}..."):
                try:
                    translated = translate_chat_text(msg_text.strip(), from_lang, to_lang)
                    tts_audio = generate_speech_bytes(translated, LANGUAGES[to_lang])
                    add_message({
                        "sender": sender_name,
                        "time": datetime.now().strftime("%H:%M"),
                        "kind": "Text",
                        "from_lang": from_lang,
                        "to_lang": to_lang,
                        "original": msg_text.strip(),
                        "translated": translated,
                        "audio_bytes": tts_audio,
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
with mode_tab_audio:
    voice_note = st.audio_input(f"Hold/Tap mic to speak in **{from_lang}** (translates to **{to_lang}**)", key="wa_mic")
    if voice_note is not None:
        raw_wav = voice_note.read()
        clip_hash = hash(raw_wav)
        if st.session_state.get("last_wa_clip") != clip_hash:
            st.session_state.last_wa_clip = clip_hash
            with st.spinner(f"Translating voice note ({from_lang} → {to_lang})..."):
                try:
                    spoken, translated = translate_media_or_audio(raw_wav, "audio/wav", from_lang, to_lang)
                    tts_audio = generate_speech_bytes(translated, LANGUAGES[to_lang])
                    add_message({
                        "sender": sender_name,
                        "time": datetime.now().strftime("%H:%M"),
                        "kind": "🎙️ Voice Note",
                        "from_lang": from_lang,
                        "to_lang": to_lang,
                        "original": spoken,
                        "translated": translated,
                        "audio_bytes": tts_audio,
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

with mode_tab_video:
    st.caption(f"Upload a short video clip (`.mp4`, `.mov`, `.webm`) spoken in **{from_lang}** to translate its speech into **{to_lang}** audio & text.")
    video_file = st.file_uploader("Upload Video Clip", type=["mp4", "mov", "webm"], key="wa_vid_up")
    if video_file is not None:
        if st.button("🎥 Send & Translate Video", type="primary", use_container_width=True):
            with st.spinner(f"Listening to video in {from_lang} & translating to {to_lang}..."):
                try:
                    vid_bytes = video_file.getvalue()
                    vid_mime = video_file.type or "video/mp4"
                    spoken_vid, translated_vid = translate_media_or_audio(vid_bytes, vid_mime, from_lang, to_lang)
                    tts_audio = generate_speech_bytes(translated_vid, LANGUAGES[to_lang])
                    add_message({
                        "sender": sender_name,
                        "time": datetime.now().strftime("%H:%M"),
                        "kind": "🎥 Video Message",
                        "from_lang": from_lang,
                        "to_lang": to_lang,
                        "original": spoken_vid,
                        "translated": translated_vid,
                        "video_bytes": vid_bytes,
                        "audio_bytes": tts_audio,
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
