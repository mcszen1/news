import streamlit as st
import openai
from openai import OpenAI
import tempfile

#openai.api_key = st.secrets["OPENAI_API_KEY"]  # Adicione sua chave de API nas Configurações de Segredo do Streamlit
client=OpenAI()

# Função para gerar o texto do release com GPT
def generate_release_with_gpt(inputs):
    
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Ou qualquer outro modelo atual que você preferir
        prompt=inputs,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript['text']

# Criação da interface do usuário no Streamlit
st.title('Gerador de Release de Imprensa com IA')
st.write('Geração a partir de uma arquivo de áudio')
st.write('Se não tiver áudio insira as informações nos campos abaixo')
uploaded_audio = st.file_uploader("Carregue o arquivo de áudio para transcrição", type=['mp3', 'wav', 'm4a', 'flac'])
if uploaded_audio is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_audio.type.split('/')[1]}") as tmpfile:
        tmpfile.write(uploaded_audio.getvalue())
        st.write("Transcrevendo o áudio... Aguarde.")
        transcription = transcribe_audio(tmpfile.name)
        st.text_area("Transcrição do áudio:", transcription, height=150)

        # Botão para gerar o release a partir da transcrição
        if st.button('Gerar Release com Áudio'):
            prompt = f"Escreva um release de imprensa com base nas informações da seguinte transcrição:\n{transcription}\nPor favor, mantenha um tom profissional e informativo."
            release_text = generate_release_with_gpt(prompt)
            st.subheader('Preview do Release gerado pela IA a partir da transcrição:')
            st.text_area('Texto do Release:', release_text, height=500)

st.write('Geração com dados inseridos pelo usuário')

# Coletando inputs do usuário
title = st.text_input('FATO EM UMA LINHA :')
date = st.time_input('QUANDO : ')
location = st.text_input('ONDE:', 'Digite o local')
introduction = st.text_area('COMO:', 'Detalhe o que aconteceu')
context = st.text_area('DESCREVA UM CONTEXTO:', 'Por que , detalhes, ect : ')
statements = st.text_area('Declarações e Citações:', 'Inclua as declarações aqui')
highlights = st.text_area('Destaques e Diferenciais:', 'Tópicos que quer destacar :')
applications = st.text_area('Detalhes adicionais :')
implications = st.text_area('Implicações e Benefícios:', 'Descreva as implicações e benefícios aqui')
contact_info = st.text_area('Informações de Contato:', 'Inclua as informações de contato aqui')

# Preparando o prompt para o GPT
prompt = (f"Escreva um release de imprensa com as seguintes informações:\n"
          f"Título: {title}\n"
          f"Data: {date}\n"
          f"Local: {location}\n"
          f"Introdução: {introduction}\n"
          f"Contexto: {context}\n"
          f"Declarações: {statements}\n"
          f"Destaques: {highlights}\n"
          f"Aplicações: {applications}\n"
          f"Implicações: {implications}\n"
          f"Informações de Contato: {contact_info}\n"
          "Por favor, mantenha um tom profissional e informativo.")

# Botão para gerar o release
if st.button('Gerar Release com Dados'):
    release_text = generate_release_with_gpt(prompt)
    st.subheader('Preview do Release gerado pela IA:')
    release_text_area = st.text_area('Texto do Release:', release_text, height=500)

    # Botão para gerar uma nova versão do release
    if st.button('Gerar Nova Versão'):
        release_text = generate_release_with_gpt(prompt)
        release_text_area = st.text_area('Texto do Release:', release_text, height=500)

    # Criando um arquivo de texto para download
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmpfile:
        tmpfile.write(release_text.encode('utf-8'))
        st.download_button(
            label="Baixar Release como TXT",
            data=release_text,
            file_name="release.txt",
            mime="text/plain"
        )