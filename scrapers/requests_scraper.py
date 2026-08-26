import time

import requests

from bs4 import BeautifulSoup

from urllib.parse import quote


BASE_URL = "https://pt.wikipedia.org/wiki/"

API_URL = "https://pt.wikipedia.org/w/api.php"


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

    nome_pagina = assunto.strip().replace(
        " ",
        "_"
    )

    return BASE_URL + quote(
        nome_pagina
    )


# Procura o título correto na Wikipédia:

def procurar_pagina(assunto):

    parametros = {
        "action": "query",
        "list": "search",
        "srsearch": assunto,
        "format": "json"
    }

    resposta = requests.get(
        API_URL,
        params=parametros,
        headers=HEADERS,
        timeout=15
    )

    if resposta.status_code != 200:

        return None

    dados = resposta.json()

    resultados = dados.get(
        "query",
        {}
    ).get(
        "search",
        []
    )

    if not resultados:

        return None

    return resultados[0]["title"]


# Coleta as páginas:

def coletar_paginas(assuntos):

    inicio = time.perf_counter()

    conteudos = []
    erros = []

    for assunto in assuntos:

        url = criar_url(
            assunto
        )

        try:

            resposta = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            # Se a página não existir:

            if resposta.status_code == 404:

                titulo = procurar_pagina(
                    assunto
                )

                if titulo:

                    url = criar_url(
                        titulo
                    )

                    resposta = requests.get(
                        url,
                        headers=HEADERS,
                        timeout=15
                    )

                else:

                    erros.append(
                        f"{assunto} (página não encontrada)"
                    )

                    continue

            # Verifica se a página foi acessada:

            if resposta.status_code != 200:

                erros.append(
                    f"{assunto} "
                    f"(HTTP {resposta.status_code})"
                )

                continue

            pagina = BeautifulSoup(
                resposta.content,
                "html.parser"
            )

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

            else:

                erros.append(
                    f"{assunto} "
                    "(página sem conteúdo)"
                )

        except requests.RequestException as erro:

            erros.append(
                f"{assunto} ({erro})"
            )

    duracao = (
        time.perf_counter() - inicio
    )

    return (
        " ".join(conteudos),
        duracao,
        erros
    )