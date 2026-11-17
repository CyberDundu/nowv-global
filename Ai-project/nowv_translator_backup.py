


import os
import io
import csv
import json
import base64
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image
from pypdf import PdfReader
from gtts import gTTS
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

HISTORY_FILE = "translation_history.csv"

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

FAST_MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash-lite"]
import wave
import numpy as np

def compress_wav_bytes(wav_bytes):
    """Shrinks browser WAV audio to lightweight 16kHz mono for near-instant upload."""
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

def translate_voice_directly(audio_bytes, source_lang, target_lang):
    prompt = (
        f"You are an expert native interpreter fluent in Hausa, Yoruba, Igbo, Fulfulde, Kanuri, "
        f"Nigerian Pidgin, English, Mandarin Chinese, French, Arabic, Swahili, and Spanish. "
        f"Listen carefully to the attached audio spoken in {source_lang}. "
        f"1. Transcribe accurately what was said in {source_lang}. "
        f"2. Translate it naturally and accurately into {target_lang}. "
        f"Return ONLY valid JSON with exact keys 'transcription' and 'translation'."
    )
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2,
    )
    small_bytes = compress_wav_bytes(audio_bytes)
    audio_part = types.Part.from_bytes(data=small_bytes, mime_type="audio/wav")

    last_error = ""

    for model_name in FAST_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[audio_part, prompt],
                config=config,
            )
            data = json.loads(response.text)
            return data.get("transcription", "").strip(), data.get("translation", "").strip()
        except Exception as e:
            last_error = str(e)
            continue
    raise RuntimeError(f"Voice translation failed: {last_error}")

def translate_text_directly(text, source_lang, target_lang):
    prompt = (
        f"You are an expert native interpreter fluent in Hausa, Yoruba, Igbo, Fulfulde, Kanuri, "
        f"Nigerian Pidgin, English, Mandarin Chinese, French, Arabic, Swahili, and Spanish. "
        f"Translate the following content from {source_lang} into {target_lang} naturally and accurately, "
        f"preserving paragraph structure and formatting. Return ONLY the translated text:\n\n{text}"
    )
    config = types.GenerateContentConfig(
        temperature=0.2,
    )
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

def scan_and_translate_image(image_bytes, source_lang, target_lang):
    """Extracts text from a photo/scan via Gemini Vision and translates it."""
    prompt = (
        f"You are an expert OCR scanner and native translator fluent in Hausa, Yoruba, Igbo, Fulfulde, Kanuri, "
        f"Nigerian Pidgin, English, Mandarin Chinese, French, Arabic, Swahili, and Spanish.\n"
        f"1. Read and extract all visible text in this image (assumed {source_lang} or mixed).\n"
        f"2. Translate the extracted text naturally and accurately into {target_lang}.\n"
        f"Return ONLY valid JSON with exact keys 'extracted_text' and 'translated_text'."
    )
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2,
    )
    pil_image = Image.open(io.BytesIO(image_bytes))
    last_error = ""

    for model_name in FAST_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[pil_image, prompt],
                config=config,
            )
            data = json.loads(response.text)
            return data.get("extracted_text", "").strip(), data.get("translated_text", "").strip()
        except Exception as e:
            last_error = str(e)
            continue
    raise RuntimeError(f"Scanner failed: {last_error}")

def extract_document_text(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    elif file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()
    return ""

def generate_speech_bytes(text, speak_code):
    if not speak_code or not text:
        return None
    tts = gTTS(text=text[:600], lang=speak_code)
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer.read()

def save_to_history(mode, source_lang, target_lang, original, translated):
    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Mode", "From", "To", "Original Text", "Translated Text"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mode,
            source_lang,
            target_lang,
            original[:200],
            translated[:200],
        ])
def get_branded_logo_b64(path):
    """Loads your exact logo file directly while preserving all original gradient colors."""
    with open(path, "rb") as img_f:
        return base64.b64encode(img_f.read()).decode()

# --- PAGE CONFIG & CUSTOM NOWV BRANDING ---
st.set_page_config(page_title="NowV.com AI Translator", page_icon="🌍", layout="centered")

logo_file = next((f for f in ["logo.png", "logo.jpg", "logo.jpeg"] if os.path.exists(f)), None)
if logo_file:
    logo_b64 = get_branded_logo_b64(logo_file)
    logo_tag = f'<img src="data:image/png;base64,{logo_b64}" style="height: 44px; width: auto; object-fit: contain;">'
else:
    logo_tag = '<div style="font-size: 2.5rem;">🌍</div>'

banner_html = (
    '<div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); '
    'padding: 1.4rem; border-radius: 14px; border: 1px solid #10b981; margin-bottom: 1.2rem; '
    'display: flex; align-items: center; gap: 1rem;">'
    f'{logo_tag}'
    '<div>'
    '<div style="color: #ffffff; font-size: 1.65rem; font-weight: 800; margin: 0;">'
    'AI Voice, Scanner & Live Chat Translator</div>'
    '<div style="color: #a7f3d0; font-size: 0.9rem; margin-top: 0.25rem;">'
    'Hausa • Yoruba • Igbo • Mandarin • English • Pidgin • French • Arabic</div>'
    '</div></div>'
)
st.markdown(banner_html, unsafe_allow_html=True)

with st.sidebar:
    if logo_file:
        st.markdown(logo_tag, unsafe_allow_html=True)
    st.header("NowV Interpreter")
    st.write("Real-time speech, camera/image scanner, live chat, and document translation.")
    st.divider()
    st.markdown("**Supported Languages:**")
    st.caption("Hausa, English, Yoruba, Igbo, Mandarin Chinese, Nigerian Pidgin, Fulfulde, Kanuri, French, Arabic, Swahili, Spanish")
    st.divider()
    st.caption("Powered by NowV.com & Gemini Multimodal AI")

if "src_idx" not in st.session_state:
    st.session_state.src_idx = 0
if "tgt_idx" not in st.session_state:
    st.session_state.tgt_idx = 1
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

lang_names = list(LANGUAGES.keys())

col1, col_mid, col2 = st.columns([5, 1.2, 5])
with col1:
    source_lang = st.selectbox("Speaker A (From)", lang_names, index=st.session_state.src_idx)
with col2:
    target_lang = st.selectbox("Speaker B (To)", lang_names, index=st.session_state.tgt_idx)
with col_mid:
    st.write("")
    st.write("")
    if st.button("⇄", help="Swap languages"):
        st.session_state.src_idx = lang_names.index(target_lang)
        st.session_state.tgt_idx = lang_names.index(source_lang)
        st.rerun()

conversation_mode = st.toggle("🔄 Auto-Swap Languages After Each Turn (Two-Way Mode)")

# --- FIVE COMPLETE TABS ---
tab_voice, tab_chat, tab_scan, tab_text, tab_doc = st.tabs([
    "🎙️ Voice",
    "💬 Live Chat",
    "📷 Image Scanner",
    "⌨️ Text",
    "📄 Document",
])

# 1. VOICE INTERPRETER TAB
with tab_voice:
    audio_recording = st.audio_input(f"Tap the microphone and speak in **{source_lang}**")
    if audio_recording is not None:
        audio_bytes = audio_recording.read()
        with st.spinner(f"Listening to {source_lang} & translating to {target_lang}..."):
            try:
                spoken_text, translated_text = translate_voice_directly(audio_bytes, source_lang, target_lang)
                speech_audio = generate_speech_bytes(translated_text, LANGUAGES[target_lang])

                save_to_history("Voice", source_lang, target_lang, spoken_text, translated_text)

                st.success(f"**🗣️ {source_lang}:** {spoken_text}")
                st.info(f"**✨ {target_lang}:** {translated_text}")

                if speech_audio:
                    st.audio(speech_audio, format="audio/mp3", autoplay=True)

                if conversation_mode:
                    st.session_state.src_idx = lang_names.index(target_lang)
                    st.session_state.tgt_idx = lang_names.index(source_lang)
                    st.toast(f"Turn switched: {target_lang} → {source_lang}")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# 2. LIVE CHAT TRANSLATOR TAB (VOICE + TEXT)
with tab_chat:
    chat_col_top1, chat_col_top2 = st.columns([4, 1])
    with chat_col_top1:
        active_speaker = st.radio(
            "Who is speaking / messaging right now?",
            [f"Speaker A ({source_lang} → {target_lang})", f"Speaker B ({target_lang} → {source_lang})"],
            horizontal=True,
        )
    with chat_col_top2:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    chat_container = st.container(height=320)
    with chat_container:
        if not st.session_state.chat_messages:
            st.caption("Start a live bilingual voice or text conversation below! Each turn is translated and spoken automatically.")
        for idx, msg in enumerate(st.session_state.chat_messages):
            with st.chat_message(msg["role"], avatar=msg["avatar"]):
                st.markdown(f"**{msg['sender']} ({msg['from_lang']} → {msg['to_lang']})** • *{msg.get('mode', 'Text')}*")
                st.write(msg["original"])
                st.success(f"✨ {msg['translated']}")
                if msg.get("audio"):
                    is_latest = idx == len(st.session_state.chat_messages) - 1
                    st.audio(msg["audio"], format="audio/mp3", autoplay=is_latest)

    is_speaker_a = active_speaker.startswith("Speaker A")
    from_l = source_lang if is_speaker_a else target_lang
    to_l = target_lang if is_speaker_a else source_lang
    sender_label = "Speaker A" if is_speaker_a else "Speaker B"

    chat_input_mode = st.radio("Chat Reply Method:", ["🎙️ Voice Audio Chat", "⌨️ Text Chat"], horizontal=True)

    if chat_input_mode == "🎙️ Voice Audio Chat":
        chat_audio_rec = st.audio_input(f"Tap mic to speak as **{sender_label}** ({from_l} → {to_l})", key="live_chat_mic")
        if chat_audio_rec is not None:
            audio_bytes = chat_audio_rec.read()
            audio_hash = hash(audio_bytes)
            if st.session_state.get("last_chat_audio_hash") != audio_hash:
                st.session_state.last_chat_audio_hash = audio_hash
                with st.spinner(f"Translating {sender_label}'s voice ({from_l} → {to_l})..."):
                    try:
                        spoken_chat, translated_chat = translate_voice_directly(audio_bytes, from_l, to_l)
                        chat_audio = generate_speech_bytes(translated_chat, LANGUAGES[to_l])

                        st.session_state.chat_messages.append({
                            "role": "user" if is_speaker_a else "assistant",
                            "avatar": "🧑🏾" if is_speaker_a else "🌍",
                            "sender": sender_label,
                            "mode": "🎙️ Voice",
                            "from_lang": from_l,
                            "to_lang": to_l,
                            "original": spoken_chat,
                            "translated": translated_chat,
                            "audio": chat_audio,
                        })
                        save_to_history("Live Audio Chat", from_l, to_l, spoken_chat, translated_chat)
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")
    else:
        chat_msg = st.text_input(
            f"Type message as **{sender_label}** ({from_l} → {to_l})...",
            key="live_chat_input",
            placeholder="Send a message to translate live...",
        )
        if st.button("Send & Translate 💬", type="primary", use_container_width=True):
            if chat_msg.strip():
                with st.spinner("Translating message..."):
                    try:
                        translated_chat = translate_text_directly(chat_msg.strip(), from_l, to_l)
                        chat_audio = generate_speech_bytes(translated_chat, LANGUAGES[to_l])

                        st.session_state.chat_messages.append({
                            "role": "user" if is_speaker_a else "assistant",
                            "avatar": "🧑🏾" if is_speaker_a else "🌍",
                            "sender": sender_label,
                            "mode": "⌨️ Text",
                            "from_lang": from_l,
                            "to_lang": to_l,
                            "original": chat_msg.strip(),
                            "translated": translated_chat,
                            "audio": chat_audio,
                        })
                        save_to_history("Live Text Chat", from_l, to_l, chat_msg.strip(), translated_chat)
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")

# 3. IMAGE & CAMERA SCANNER TAB
with tab_scan:
    scan_method = st.radio("Choose Scanner Input:", ["📁 Upload Picture / Receipt / Sign", "📸 Snap Photo with Camera"], horizontal=True)
    image_file = None

    if scan_method == "📁 Upload Picture / Receipt / Sign":
        image_file = st.file_uploader("Upload an image (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
    else:
        image_file = st.camera_input("Point your camera at text, a menu, label, or receipt")

    if image_file is not None:
        st.image(image_file, caption="Scanned Image", use_container_width=True)
        if st.button("🔍 Scan & Translate Image", type="primary", use_container_width=True):
            with st.spinner(f"Scanning image & translating to {target_lang}..."):
                try:
                    img_bytes = image_file.getvalue()
                    extracted, translated_img = scan_and_translate_image(img_bytes, source_lang, target_lang)
                    img_audio = generate_speech_bytes(translated_img, LANGUAGES[target_lang])

                    save_to_history("Image Scan", source_lang, target_lang, extracted, translated_img)

                    st.success(f"**🔍 Detected Text:**\n\n{extracted}")
                    st.info(f"**✨ {target_lang} Translation:**\n\n{translated_img}")

                    if img_audio:
                        st.audio(img_audio, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

# 4. TEXT TRANSLATOR TAB
with tab_text:
    typed_input = st.text_area(
        f"Type your message in **{source_lang}**",
        placeholder=f"Enter text in {source_lang} to translate into {target_lang}...",
        height=110,
    )
    if st.button("✨ Translate Text", type="primary", use_container_width=True):
        if not typed_input.strip():
            st.warning("Please type a message first.")
        else:
            with st.spinner(f"Translating to {target_lang}..."):
                try:
                    translated_text = translate_text_directly(typed_input.strip(), source_lang, target_lang)
                    speech_audio = generate_speech_bytes(translated_text, LANGUAGES[target_lang])

                    save_to_history("Text", source_lang, target_lang, typed_input.strip(), translated_text)

                    st.success(f"**⌨️ {source_lang}:** {typed_input.strip()}")
                    st.info(f"**✨ {target_lang}:** {translated_text}")

                    if speech_audio:
                        st.audio(speech_audio, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

# 5. DOCUMENT TRANSLATOR TAB
with tab_doc:
    uploaded_doc = st.file_uploader(
        f"Upload a **.txt** or **.pdf** document in **{source_lang}**",
        type=["txt", "pdf"],
    )
    if uploaded_doc is not None:
        extracted_text = extract_document_text(uploaded_doc)
        if not extracted_text:
            st.warning("Could not find readable text inside this file.")
        else:
            with st.expander("👀 Preview Extracted Original Text"):
                st.text(extracted_text[:1500] + ("..." if len(extracted_text) > 1500 else ""))

            if st.button("📄 Translate Entire Document", type="primary", use_container_width=True):
                with st.spinner(f"Translating '{uploaded_doc.name}' into {target_lang}..."):
                    try:
                        translated_doc = translate_text_directly(extracted_text, source_lang, target_lang)
                        speech_audio = generate_speech_bytes(translated_doc, LANGUAGES[target_lang])

                        save_to_history("Document", source_lang, target_lang, f"[{uploaded_doc.name}] {extracted_text[:80]}", translated_doc)

                        st.subheader(f"✨ Translated Document ({target_lang})")
                        st.text_area("Result", value=translated_doc, height=220)

                        if speech_audio:
                            st.caption("🔊 Audio Preview (Opening section):")
                            st.audio(speech_audio, format="audio/mp3")

                        base_name = os.path.splitext(uploaded_doc.name)[0]
                        st.download_button(
                            label=f"⬇️ Download Translated File ({base_name}_{target_lang}.txt)",
                            data=translated_doc.encode("utf-8"),
                            file_name=f"{base_name}_{target_lang}.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")

st.divider()

# --- SAVED TRANSLATION HISTORY ---
st.subheader("📜 Translation History")
if os.path.exists(HISTORY_FILE):
    df = pd.read_csv(HISTORY_FILE, on_bad_lines="skip")
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)

    col_dl, col_clr = st.columns(2)
    with col_dl:
        st.download_button(
            label="⬇️ Download History (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="nowv_translation_history.csv",
            mime="text/csv",
        )
    with col_clr:
        if st.button("🗑️ Clear History"):
            os.remove(HISTORY_FILE)
            st.rerun()
else:
    st.write("No translations recorded yet. Use any tab above to begin!")
