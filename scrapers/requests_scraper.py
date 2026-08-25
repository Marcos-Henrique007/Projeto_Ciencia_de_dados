import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


BASE_URL = "https://pt.wikipedia.org/wiki/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


def criar_url(assunto):
    nome_pagina = assunto.strip().replace(" ", "_")

    return BASE_URL + quote(nome_pagina)


def coletar_paginas(assuntos):
    inicio = time.perf_counter()

    conteudos = []
    erros = []

    for assunto in assuntos:

        url = criar_url(assunto)

        try:

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            if resposta.status_code != 200:
                erros.append(
                    f"{assunto} (HTTP {resposta.status_code})"
                )
                continue

            pagina = BeautifulSoup(
                resposta.content,
                "html.parser"
            )

            paragrafos = pagina.find_all("p")

            texto = " ".join(
                paragrafo.get_text(" ", strip=True)
                for paragrafo in paragrafos
            )

            if texto:
                conteudos.append(texto)

        except requests.RequestException as erro:

            erros.append(
                f"{assunto} ({erro})"
            )

    duracao = time.perf_counter() - inicio

    return " ".join(conteudos), duracao, erros