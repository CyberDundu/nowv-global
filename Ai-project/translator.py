import os
import subprocess
import io
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load your GEMINI_API_KEY from .env
load_dotenv()
client = genai.Client()

LISTEN_CODES = {
    "english": "en-NG",
    "hausa": "ha-NG",
    "yoruba": "yo-NG",
    "igbo": "ig-NG",
    "pidgin": "en-NG",
    "french": "fr-FR",
    "arabic": "ar-SA"
}

SPEAK_CODES = {
    "hausa": "ha",
    "yoruba": "yo",
    "english": "en",
    "french": "fr",
    "arabic": "ar",
    "swahili": "sw"
}

def listen_smart(source_language, max_seconds=8, silence_threshold=300, silence_duration=1.0):
    """Records from your mic and stops automatically 1 second after you finish speaking."""
    sample_rate = 16000
    chunk_size = int(sample_rate * 0.1)
    frames = []
    silent_chunks = 0
    has_spoken = False

    print(f"\n🎤 Speak in {source_language} now...")
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16") as stream:
        for _ in range(int(max_seconds * 10)):
            data, _ = stream.read(chunk_size)
            frames.append(data.copy())
            volume = np.abs(data).mean()

            if volume > silence_threshold:
                has_spoken = True
                silent_chunks = 0
            elif has_spoken:
                silent_chunks += 1
                if silent_chunks >= int(silence_duration * 10):
                    break

    audio_bytes = io.BytesIO()
    with wave.open(audio_bytes, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(np.concatenate(frames).tobytes())
    audio_bytes.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_bytes) as source:
        audio_data = recognizer.record(source)

    lang_code = LISTEN_CODES.get(source_language.lower(), "en-NG")
    return recognizer.recognize_google(audio_data, language=lang_code)

def translate_fast(text, source_language, target_language):
    """Translates naturally between Nigerian and global languages with zero thinking lag."""
    prompt = (
        f"You are a fluent native translator specializing in Nigerian languages "
        f"(Hausa, Igbo, Yoruba, Nigerian Pidgin, Fulfulde, Kanuri) and global languages. "
        f"Translate the following from {source_language} to {target_language} naturally and accurately. "
        f"Return ONLY the translated text:\n{text}"
    )
    fast_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        temperature=0.2
    )

    for model_name in ["gemini-3.5-flash", "gemini-3.0-flash"]:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=fast_config
            )
            return response.text.strip()
        except Exception:
            continue
    raise RuntimeError("Translation servers are temporarily busy. Please try again.")

def speak_translation(text, language_name):
    """Speaks the translation using gTTS, with macOS native voice fallback for Igbo/Pidgin."""
    lang_key = language_name.lower().strip()
    if lang_key in SPEAK_CODES:
        try:
            tts = gTTS(text=text, lang=SPEAK_CODES[lang_key])
            audio_output_file = "translation.mp3"
            tts.save(audio_output_file)
            subprocess.run(["afplay", audio_output_file])
            return
        except Exception:
            pass
    subprocess.run(["say", text])

if __name__ == "__main__":
    print("=== ⚡ NOWV NIGERIAN & GLOBAL VOICE TRANSLATOR ===")
    print("Supported: Hausa | Igbo | Yoruba | Pidgin | Fulfulde | Kanuri | English | French | Arabic")
    source_lang = input("\nSource language: ")
    target_lang = input("Target language: ")

    while True:
        try:
            spoken_text = listen_smart(source_lang)
            print(f"🗣️ Original ({source_lang}): {spoken_text}")

            translated = translate_fast(spoken_text, source_lang, target_lang)
            print(f"✨ Translation ({target_lang}): {translated}")

            speak_translation(translated, target_lang)

            again = input("\nPress Enter to translate again (or type 'q' to quit): ")
            if again.lower() == "q":
                break

        except sr.UnknownValueError:
            print("❌ Couldn't catch that clearly. Press Enter to try speaking again.")
            input()
        except Exception as e:
            print(f"⚠️ Error: {e}")
            break