import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

from wordcloud import WordCloud

from scrapers.requests_scraper import (
    coletar_paginas as coletar_requests
)

from scrapers.scrapy_scraper import (
    coletar_paginas as coletar_scrapy
)

from utils.text_processing import (
    limpar_texto,
    remover_stopwords,
    contar_palavra
)


# Configuração:

st.set_page_config(
    page_title="Web Scraping - Wikipédia"
)


# Funções da interface:

def gerar_nuvem(texto):

    nuvem = WordCloud(
        width=700,
        height=350,
        background_color="white"
    ).generate(texto)

    figura, eixo = plt.subplots(
        figsize=(8, 4)
    )

    eixo.imshow(
        nuvem,
        interpolation="bilinear"
    )

    eixo.axis("off")

    return figura


def mostrar_resultado(
    nome_metodo,
    conteudo,
    duracao,
    palavra,
    erros
):

    if erros:

        for erro in erros:

            st.warning(
                f"Não foi possível coletar: {erro}"
            )

    if not conteudo:

        st.error(
            f"O método {nome_metodo} "
            "não conseguiu coletar conteúdo."
        )

        return

    texto_limpo = limpar_texto(
        conteudo
    )

    texto_nuvem = remover_stopwords(
        texto_limpo
    )

    if not texto_nuvem:

        st.error(
            "Não foi encontrado conteúdo suficiente."
        )

        return

    quantidade = contar_palavra(
        texto_nuvem,
        palavra
    )

    st.subheader(
        nome_metodo
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Tempo",
            f"{duracao:.2f} s"
        )

    with col2:

        st.metric(
            "Ocorrências",
            quantidade
        )

    st.write(
        f"A palavra **'{palavra}'** "
        f"apareceu **{quantidade} vezes**."
    )

    figura = gerar_nuvem(
        texto_nuvem
    )

    st.pyplot(
        figura,
        width="stretch"
    )

    plt.close(figura)


# Tela principal:

st.title(
    "Web Scraping na Wikipédia"
)

st.caption(
    "Requests + BeautifulSoup x Scrapy"
)


entrada = st.text_input(
    "Digite 5 assuntos separados por vírgula:",
    placeholder=(
        "Ciência de Dados, Engenharia de Software, "
        "Aprendizado de Máquina, Banco de Dados, UFRN"
    )
)


palavra_busca = st.text_input(
    "Digite uma palavra para pesquisar:"
)


assuntos = [
    assunto.strip()
    for assunto in entrada.split(",")
    if assunto.strip()
]


coluna1, coluna2 = st.columns(2)


with coluna1:

    executar_requests = st.button(
        "Requests + BeautifulSoup",
        use_container_width=True
    )


with coluna2:

    executar_scrapy = st.button(
        "Scrapy",
        use_container_width=True
    )


# Requests com BeautifulSoup:

if executar_requests:

    if len(assuntos) != 5:

        st.warning(
            "Digite exatamente 5 assuntos."
        )

    elif not palavra_busca.strip():

        st.warning(
            "Digite uma palavra para pesquisar."
        )

    else:

        with st.spinner(
            "Executando Requests + BeautifulSoup..."
        ):

            conteudo, duracao, erros = (
                coletar_requests(assuntos)
            )

        mostrar_resultado(
            "Requests + BeautifulSoup",
            conteudo,
            duracao,
            palavra_busca,
            erros
        )


# Scrapy:

if executar_scrapy:

    if len(assuntos) != 5:

        st.warning(
            "Digite exatamente 5 assuntos."
        )

    elif not palavra_busca.strip():

        st.warning(
            "Digite uma palavra para pesquisar."
        )

    else:

        with st.spinner(
            "Executando Scrapy..."
        ):

            conteudo, duracao, erros = (
                coletar_scrapy(assuntos)
            )

        mostrar_resultado(
            "Scrapy",
            conteudo,
            duracao,
            palavra_busca,
            erros
        )