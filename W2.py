import base64
import streamlit as st
from openai import OpenAI
import os
from io import BytesIO

# Função para salvar o arquivo de áudio carregado localmente
def save_uploaded_audio(uploaded_file):
    filename = uploaded_file.name
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Use getbuffer() para acessar o conteúdo do arquivo
    return filename

# Função para realizar a transcrição do áudio com a API do Whisper
def analyze_audio_with_whisper(audio_path):
    client = OpenAI()  # Inicializa o cliente da OpenAI
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file, response_format="text"
        )
    return transcript  # Retorna o texto transcrito

# Interface do usuário para upload de arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio...", type=["ogg","wav","mp3"])
if uploaded_file:
    # Salvar o arquivo de áudio carregado localmente
    audio_filename = save_uploaded_audio(uploaded_file)

    # Exibir o áudio no Streamlit para que o usuário possa ouvir
    file_type = uploaded_file.type.split('/')[1]  # Obter a extensão do tipo de arquivo
    st.audio(audio_filename, format=f'audio/{file_type}', start_time=0)

    # Chamar a função de análise de áudio e obter a transcrição
    description = analyze_audio_with_whisper(audio_filename)

    # Exibir a transcrição do áudio
    st.text("Transcrição do áudio:")
    st.text(description)
    
    transcription_bytes = BytesIO(description.encode('latin-1'))
    st.download_button(
                label="Baixar transcrição como texto",
                data=transcription_bytes,
                file_name='transcription.txt',
                mime='text/plain'
            )
   

