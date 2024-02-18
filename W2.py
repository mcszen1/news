import base64
import streamlit as st
from openai import OpenAI

# Função para salvar o arquivo de áudio carregado localmente
def save_uploaded_audio(uploaded_file_content, filename):
    with open(filename, "wb") as f:
        f.write(uploaded_file_content)
    return filename

# Função para realizar a transcrição do áudio com a API do Whisper
def analyze_audio_with_whisper(audio_path):
    client = OpenAI()  # Inicializa o cliente da OpenAI
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript['text']  # Retorna o texto transcrito

# Interface do usuário para upload de arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio...", type=["mp3", "wav", "ogg", "flac"])
if uploaded_file:
    # Salvar o arquivo de áudio carregado localmente
    audio_filename = save_uploaded_audio(uploaded_file.read(), "temp_audio.mp3")

    # Exibir o áudio no Streamlit para que o usuário possa ouvir
    st.audio(audio_filename, format='audio/mp3', start_time=0)

    # Chamar a função de análise de áudio e obter a transcrição
    description = analyze_audio_with_whisper(audio_filename)

    # Exibir a transcrição do áudio
    st.text("Transcrição do áudio:")
    st.text(description)

