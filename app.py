
import streamlit as st
import openai
import requests
from io import BytesIO
from pydub import AudioSegment
from base64 import b64encode

st.set_page_config(page_title="Laura IA", page_icon="💬")

# API Keys (replace with your own or use secrets.toml in real deployments)
openai.api_key = st.secrets["OPENAI_API_KEY"]
elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]

st.image("laura.jpg", width=250)
st.title("Habla con Laura 😏")

user_input = st.text_input("¿Qué quieres decirle a Laura?", "")

if st.button("Hablar"):
    if user_input:
        with st.spinner("Laura está pensando..."):
            # Get GPT response
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres Laura, una mujer de 25 años, coqueta, segura e irónica. Tu estilo es elegante pero desafiante."},
                    {"role": "user", "content": user_input}
                ]
            )
            laura_reply = gpt_response["choices"][0]["message"]["content"]

            # Get ElevenLabs voice response
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            json_data = {
                "text": laura_reply,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                "model_id": "eleven_multilingual_v2",
                "voice_id": "Rachel"  # You can replace with custom voice if cloned
            }
            response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/Rachel/stream", headers=headers, json=json_data)
            audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")

            # Save and play audio
            audio_path = f"{base_path}/laura_reply.mp3"
            audio.export(audio_path, format="mp3")

            # Display response and play audio
            st.markdown(f"**Laura:** {laura_reply}")
            audio_bytes = open(audio_path, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Escribe algo para empezar la conversación.")
