import streamlit as st
import matplotlib.pyplot as plt

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
    page_title="Web Scraping - Wikipédia",
    page_icon="",
    layout="centered"
)


# Funções da interface:

def gerar_nuvem(texto):

    nuvem = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(texto)

    figura, eixo = plt.subplots(
        figsize=(9, 4.5)
    )

    eixo.imshow(
        nuvem,
        interpolation="bilinear"
    )

    eixo.axis("off")

    return figura


def processar_resultado(
    nome_metodo,
    conteudo,
    duracao,
    palavra,
    erros,
    progresso
):

    # Mostra o processamento:

    with st.status(
        "Processando...",
        expanded=True
    ) as status:

        # Mostra as etapas realizadas:

        for mensagem in progresso:

            st.write(
                mensagem
            )


        # Mostra os erros encontrados:

        if erros:

            for erro in erros:

                st.error(
                    erro
                )


        # Verifica se algum conteúdo foi coletado:

        if not conteudo:

            status.update(
                label="Erro durante o processamento",
                state="error"
            )

            st.error(
                f"O método {nome_metodo} "
                "não conseguiu coletar conteúdo."
            )


            # Mostra detalhes do erro:

            if erros:

                st.write(
                    "Detalhes do erro:"
                )

                for erro in erros:

                    st.error(
                        erro
                    )

            else:

                st.warning(
                    "O método terminou a execução, "
                    "mas não retornou nenhum conteúdo."
                )

            return


        # Processa o texto:

        st.write(
            "Processando texto..."
        )

        texto_limpo = limpar_texto(
            conteudo
        )


        # Conta a palavra pesquisada:

        st.write(
            "Contando a palavra pesquisada..."
        )

        quantidade = contar_palavra(
            texto_limpo,
            palavra
        )


        # Remove as stopwords:

        st.write(
            "Removendo stopwords..."
        )

        texto_nuvem = remover_stopwords(
            texto_limpo
        )


        # Verifica se existe texto para a nuvem:

        if not texto_nuvem:

            status.update(
                label="Não foi possível gerar a nuvem",
                state="error"
            )

            st.error(
                "Não foi encontrado conteúdo suficiente "
                "após o processamento."
            )

            return


        # Gera a nuvem:

        st.write(
            "Gerando nuvem de palavras..."
        )

        figura = gerar_nuvem(
            texto_nuvem
        )


        # Finaliza o processamento:

        status.update(
            label="Processamento concluído!",
            state="complete"
        )


    # Mostra o resultado:

    st.subheader(
        nome_metodo
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Tempo de execução",
            f"{duracao:.2f} s"
        )


    with col2:

        st.metric(
            f"Ocorrências de '{palavra}'",
            quantidade
        )


    st.write(
        f"A palavra **{palavra}** "
        f"apareceu **{quantidade} vezes**."
    )


    st.write(
        "Nuvem de palavras:"
    )


    st.pyplot(
        figura
    )


    plt.close(
        figura
    )


# Tela principal:

st.title(
    "Web Scraping na Wikipédia"
)

st.write(
    "Comparação entre Requests + BeautifulSoup "
    "e Scrapy utilizando cinco páginas da Wikipédia."
)


st.divider()


entrada = st.text_area(
    "Digite exatamente 5 assuntos diferentes:",
    placeholder=(
        "Ciência de Dados, Engenharia de Software, "
        "Aprendizado de Máquina, Banco de Dados, UFRN"
    )
)


palavra_busca = st.text_input(
    "Digite uma palavra para pesquisar:"
)


st.divider()


# Organiza os assuntos digitados:

assuntos = [

    assunto.strip()

    for assunto in entrada.split(",")

    if assunto.strip()

]


# Botões:

coluna1, coluna2 = st.columns(2)


with coluna1:

    executar_requests = st.button(
        "Executar Requests + BeautifulSoup",
        use_container_width=True
    )


with coluna2:

    executar_scrapy = st.button(
        "Executar Scrapy",
        use_container_width=True
    )


# Validação dos dados:

def validar_entrada():

    st.write(
        "Validando os dados..."
    )


    # Verifica se foram digitados exatamente 5 assuntos:

    if len(assuntos) != 5:

        st.warning(
            "Você precisa informar exatamente "
            "5 assuntos."
        )

        return False


    # Verifica se os assuntos são diferentes:

    assuntos_normalizados = [

        assunto.lower()

        for assunto in assuntos

    ]


    if len(
        set(assuntos_normalizados)
    ) != 5:

        st.warning(
            "Os 5 assuntos precisam ser diferentes."
        )

        return False


    # Verifica a palavra pesquisada:

    if not palavra_busca.strip():

        st.warning(
            "Digite também uma palavra para pesquisar."
        )

        return False


    return True


# Requests + BeautifulSoup:

if executar_requests:

    if validar_entrada():

        with st.spinner(
            "Executando Requests + BeautifulSoup..."
        ):

            (
                conteudo,
                duracao,
                erros,
                progresso
            ) = coletar_requests(
                assuntos
            )


        st.divider()


        processar_resultado(
            "Requests + BeautifulSoup",
            conteudo,
            duracao,
            palavra_busca,
            erros,
            progresso
        )


# Scrapy:

if executar_scrapy:

    if validar_entrada():

        with st.spinner(
            "Executando Scrapy..."
        ):

            (
                conteudo,
                duracao,
                erros,
                progresso
            ) = coletar_scrapy(
                assuntos
            )


        st.divider()


        processar_resultado(
            "Scrapy",
            conteudo,
            duracao,
            palavra_busca,
            erros,
            progresso
        )