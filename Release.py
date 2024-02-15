import streamlit as st
from openai import OpenAI
import tempfile

#openai.api_key = st.secrets["OPENAI_API_KEY"]  # Adicione sua chave de API nas Configurações de Segredo do Streamlit
client=OpenAI()

# Função para gerar o texto do release com GPT
def generate_release_with_gpt(inputs):
    
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",  # Ou qualquer outro modelo atual que você preferir
        prompt=inputs,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return ['choices'][0]['text']

# Criação da interface do usuário no Streamlit
st.title('Gerador de Release de Imprensa com IA')

# Coletando inputs do usuário
title = st.text_input('Título do Release:', 'Digite aqui o título')
date = st.text_input('Data de Publicação:', 'Digite a data')
location = st.text_input('Local:', 'Digite o local')
introduction = st.text_area('Introdução (Lead):', 'Digite a introdução')
context = st.text_area('Contexto Detalhado:', 'Digite o contexto')
statements = st.text_area('Declarações e Citações:', 'Inclua as declarações aqui')
highlights = st.text_area('Destaques e Diferenciais:', 'Descreva os destaques aqui')
applications = st.text_area('Como (Aplicações):', 'Explique as aplicações aqui')
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
if st.button('Gerar Release com IA'):
    release_text = generate_release_with_gpt(prompt)
    st.subheader('Preview do Release gerado pela IA:')
    release_text_area = st.text_area('Texto do Release:', release_text, height=300)

    # Botão para gerar uma nova versão do release
    if st.button('Gerar Nova Versão'):
        release_text = generate_release_with_gpt(prompt)
        release_text_area = st.text_area('Texto do Release:', release_text, height=300)

    # Criando um arquivo de texto para download
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmpfile:
        tmpfile.write(release_text.encode('utf-8'))
        st.download_button(
            label="Baixar Release como TXT",
            data=release_text,
            file_name="release.txt",
            mime="text/plain"
        )
