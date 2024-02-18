import streamlit as st
from pydub import AudioSegment
from openai import OpenAI

# Certifique-se de que pydub esteja instalado: pip install pydub

# Função para salvar o arquivo de áudio carregado localmente
def save_uploaded_audio(uploaded_file):
    filename = uploaded_file.name
    original_path = f"temp_{filename}"
    with open(original_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Use getbuffer() para acessar o conteúdo do arquivo
    return original_path, filename

# Função para converter o arquivo de áudio para formato .ogg usando pydub
def convert_audio_to_ogg(original_path, filename):
    # Determinar o formato do arquivo original com base na extensão do nome do arquivo
    format = filename.split('.')[-1]
    try:
        original_audio = AudioSegment.from_file(original_path, format=format)
        output_path = original_path.split('.')[0] + ".ogg"
        original_audio.export(output_path, format="ogg")
        return output_path
    except Exception as e:
        st.error(f"Erro ao converter arquivo: {e}")
        return None

# Função para realizar a transcrição do áudio com a API do Whisper
def analyze_audio_with_whisper(audio_path):
    client = OpenAI()  # Inicializa o cliente da OpenAI
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription  # Retorna o texto transcrito

# Interface do usuário para upload de arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio...", type=["mp3", "wav", "ogg", "flac", "m4a", "mp4", "mpeg", "mpga", "oga", "webm"])
if uploaded_file:
    # Salvar o arquivo de áudio carregado localmente
    original_audio_path, filename = save_uploaded_audio(uploaded_file)

    # Converter o arquivo de áudio para .ogg
    ogg_audio_path = convert_audio_to_ogg(original_audio_path, filename)
    if ogg_audio_path:
        # Exibir o áudio no Streamlit para que o usuário possa ouvir
        st.audio(ogg_audio_path, format='audio/ogg', start_time=0)

        # Chamar a função de análise de áudio e obter a transcrição
        description = analyze_audio_with_whisper(ogg_audio_path)

        # Exibir a transcrição do áudio
        st.text("Transcrição do áudio:")
        st.text(description)
