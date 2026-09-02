import time

import requests

from bs4 import BeautifulSoup

from urllib.parse import quote


# URL base da Wikipédia:

BASE_URL = (
    "https://pt.wikipedia.org/wiki/"
)


# Identificação do navegador:

HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )

}


# Cria a URL da página:

def criar_url(assunto):

    nome_pagina = (
        assunto.strip()
        .replace(" ", "_")
    )

    return (
        BASE_URL
        + quote(nome_pagina)
    )


# Coleta as páginas:

def coletar_paginas(
    assuntos
):

    inicio = time.perf_counter()

    conteudos = []

    erros = []

    progresso = []


    progresso.append(
        "Iniciando coleta com Requests + BeautifulSoup..."
    )


    for indice, assunto in enumerate(
        assuntos,
        start=1
    ):

        progresso.append(
            f"Processando página {indice}/5: "
            f"{assunto}"
        )


        url = criar_url(
            assunto
        )


        progresso.append(
            f"Acessando: {url}"
        )


        try:

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )


            # Trata página inexistente:

            if resposta.status_code == 404:

                erros.append(
                    f"Erro 404: a página "
                    f"'{assunto}' não foi encontrada."
                )

                progresso.append(
                    f"Página não encontrada: {assunto}"
                )

                continue


            # Trata outros erros HTTP:

            if resposta.status_code != 200:

                erros.append(
                    f"Erro HTTP {resposta.status_code}: "
                    f"{assunto}"
                )

                progresso.append(
                    f"Erro ao acessar: {assunto}"
                )

                continue


            progresso.append(
                f"Página encontrada: {assunto}"
            )


            # Analisa o HTML:

            progresso.append(
                "Analisando o HTML..."
            )


            pagina = BeautifulSoup(
                resposta.content,
                "html.parser"
            )


            # Extrai os parágrafos:

            paragrafos = pagina.find_all(
                "p"
            )


            texto = " ".join(
                paragrafo.get_text(
                    " ",
                    strip=True
                )
                for paragrafo in paragrafos
            )


            if texto:

                conteudos.append(
                    texto
                )

                progresso.append(
                    f"Conteúdo extraído: {assunto}"
                )

            else:

                erros.append(
                    f"A página '{assunto}' "
                    "não possui conteúdo textual."
                )


        except requests.RequestException as erro:

            erros.append(
                f"Erro ao acessar '{assunto}': "
                f"{erro}"
            )

            progresso.append(
                f"Falha na requisição: {assunto}"
            )


    duracao = (
        time.perf_counter()
        - inicio
    )


    progresso.append(
        "Coleta finalizada."
    )


    return (
        " ".join(conteudos),
        duracao,
        erros,
        progresso
    )