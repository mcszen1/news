import feedparser
import streamlit as st

def coletar_noticias(termo, limite=20):
    url = f"https://news.google.com/rss/search?q={termo}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
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

def main():
    st.title("Coletor de Notícias do Google News")
    
    termo = st.text_input("Insira o termo de busca:", value="criptomoedas")
    if st.button("Buscar Notícias"):
        resultados = coletar_noticias(termo)
        st.write("### Resultados:")
        for res in resultados:
            st.write(f"- {res[0]} ({res[1]})")

if __name__ == "__main__":
    main()
