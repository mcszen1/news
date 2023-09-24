import pandas as pd
import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
import string
import io

# Importando bibliotecas adicionais
from docx import Document
import PyPDF2
import requests
from bs4 import BeautifulSoup

st.image('labcom_logo_preto.jpg')

st.title('Analista de Textos')

st.header('Palavras Frequentes')
st.write('A partir de um arquivo ou URL, vamos gerar um gráfico com as palavras mais frequentes')
numero = st.slider('Quantas palavras frequentes quer no gráfico?', 5, 50, 25, 5)

# Função para converter DOCX em texto
def docx_to_text(content):
    doc = Document(io.BytesIO(content))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Função para converter PDF em texto
def pdf_to_text(content):
    pdf_file = io.BytesIO(content)
    reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(reader.numPages):
        text += reader.getPage(page_num).extractText()
    return text

# Função para converter URL em texto
def url_to_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def bytestotext(filename, file_type):
    if file_type == "txt":
        return filename.getvalue().decode('utf-8')
    elif file_type == "docx":
        return docx_to_text(filename.getvalue())
    elif file_type == "pdf":
        return pdf_to_text(filename.getvalue())
    else:
        raise ValueError("Unsupported file type")

def frequentes(text, numero):
    # Tokenização
    translator = str.maketrans('', '', string.punctuation)
    words = [word.lower().translate(translator) for word in text.split()]

    with open('stop_words_brazil.txt', mode='r', encoding='utf-8') as file:
        stopw1 = [str(s.strip()) for s in file.readlines()]
    textos = [t for t in words if t.lower() not in stopw1 if len(t) > 2]

    # Contagem de palavras
    word_count = Counter(textos)

    # Liste as palavras mais frequentes
    return word_count.most_common(numero)

file_types = ["txt", "docx", "pdf"]
filename = st.file_uploader('Insira seu arquivo', type=file_types)
url = st.text_input("Ou insira uma URL:")

if filename:
    text = bytestotext(filename, filename.type.split('/')[-1])
    top_words = frequentes(text, numero)

    words, counts = zip(*top_words)
    plt.figure(figsize=(12,8))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Contagem')
    plt.ylabel('Palavras')
    plt.title(str(numero)+' Palavras mais frequentes')
    plt.gca().invert_yaxis()  # para exibir a palavra mais comum no topo
    st.pyplot(plt)

elif url:
    text = url_to_text(url)
    top_words = frequentes(text, numero)

    words, counts = zip(*top_words)
    plt.figure(figsize=(12,8))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Contagem')
    plt.ylabel('Palavras')
    plt.title(str(numero)+' Palavras mais frequentes')
    plt.gca().invert_yaxis()  # para exibir a palavra mais comum no topo
    st.pyplot(plt)

else:
    st.write('Com seu arquivo ou URL vou mostrar um gráfico com as palavras mais frequentes')
