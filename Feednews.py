import feedparser
import streamlit as st
from urllib.parse import quote_plus


def coletar_noticias(termo, limite=20):
    termo_codificado = quote_plus(termo)  # codificar o termo de pesquisa
    url = f"https://news.google.com/rss/search?q={termo_codificado}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
    feed = feedparser.parse(url)
    entradas = feed.entries[:limite]
    noticias = []
    for entrada in entradas:
        titulo = entrada.title
        link = entrada.link
        data = entrada.published
        link_clicavel = f"[{titulo}]({link})"
        noticias.append([link_clicavel, data])
    return noticias

def gerar_codigo_incorporacao(resultados):
    html = '<ul>'
    for res in resultados:
        if "Title" in res and "URL" in res and "Date Created" in res:
            titulo = res["Title"]
            link = res["URL"]
            data = res["Date Created"]
            html += f'<li><a href="{link}">{titulo}</a> ({data})</li>'
    html += '</ul>'
    return html



def main():
    st.image('labcom_logo_preto.jpg')

    st.title('AutoNEWS')

    st.header('Coletor de notícias do LABCOM')
    st.write('Digite um tópico e dê ENTER. Depois clique em BUSCAR NOTÍCIAS')
        
    termo = st.text_input("Insira o termo de busca:", value="criptomoedas")
    if st.button("Buscar Notícias"):
        resultados = coletar_noticias(termo)
        st.write("### Resultados:")
        for res in resultados:
            st.write(f"- {res[0]} ({res[1]})")

        st.write(resultados)

        # Gerar e exibir o código de incorporação
        embed_code = gerar_codigo_incorporacao(resultados)
        st.write("### Código de Incorporação:")
        st.code(embed_code, language="html")

if __name__ == "__main__":
    main()
