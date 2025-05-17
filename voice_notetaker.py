import openai
import streamlit as st
import tempfile
import speech_recognition as sr
import pyttsx3
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Voice Notetaker", layout="centered")

st.title("🎙️ Voice Notetaker AI")
st.write("Press the button, speak, and get a smart summary of your thoughts.")

if "summary" not in st.session_state:
    st.session_state.summary = ""

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", file=f)
    return transcript['text']

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this in 1–2 sentences for notes."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Upload audio file or record live (basic mobile-friendly way)
uploaded_file = st.file_uploader("Upload a WAV audio file", type=["wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.audio(temp_path, format='audio/wav')

    if st.button("🧠 Transcribe and Summarize"):
        transcript = transcribe_audio(temp_path)
        summary = summarize_text(transcript)
        st.session_state.summary = summary
        st.success("✅ Summary ready!")

        st.subheader("📝 Summary")
        st.write(summary)

        if st.button("🔊 Read Back"):
            speak_text(summary)

        os.remove(temp_path)

---

### **2. Add Secrets File for Your API Key**

Create a file named `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-xxxxxx"
