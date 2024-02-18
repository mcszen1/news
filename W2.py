import base64
import streamlit as st
from openai import OpenAI
import os

# Função para salvar o arquivo de áudio carregado localmente
def save_uploaded_audio(uploaded_file_content, uploaded_file_type):
    extension = uploaded_file_type.split('/')[1]  # Obter a extensão do tipo de arquivo
    filename = f"temp_audio.{extension}"
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
uploaded_file = st.file_uploader("Escolha um arquivo de áudio...", type=["mp3", "wav", "ogg", "flac", "m4a", "mp4", "mpeg", "mpga", "oga", "webm"])
if uploaded_file:
    # Determinar a extensão do arquivo e definir o formato de mídia adequado
    file_extension = uploaded_file.name.split('.')[-1]
    audio_format = f'audio/{file_extension}' if file_extension != 'mpga' else 'audio/mpeg'

    # Salvar o arquivo de áudio carregado localmente
    audio_filename = save_uploaded_audio(uploaded_file.read(), f"temp_audio.{file_extension}")

    # Exibir o áudio no Streamlit para que o usuário possa ouvir
    st.audio(audio_filename, format=audio_format, start_time=0)

    # Chamar a função de análise de áudio e obter a transcrição
    try:
        description = analyze_audio_with_whisper(audio_filename)
        # Exibir a transcrição do áudio
        st.text("Transcrição do áudio:")
        st.text(description)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo de áudio: {str(e)}")

   

