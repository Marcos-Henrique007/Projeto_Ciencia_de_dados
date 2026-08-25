import time

import crochet

from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from urllib.parse import quote


crochet.setup()


BASE_URL = "https://pt.wikipedia.org/wiki/"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0 Safari/537.36"
)


def criar_url(assunto):
    nome_pagina = assunto.strip().replace(" ", "_")

    return BASE_URL + quote(nome_pagina)


class PaginasWikipedia(Spider):

    name = "paginas_wikipedia"

    custom_settings = {
        "USER_AGENT": USER_AGENT,
        "LOG_LEVEL": "ERROR",
        "DOWNLOAD_TIMEOUT": 15,
        "TWISTED_REACTOR":
            "twisted.internet.selectreactor.SelectReactor"
    }

    def __init__(self, urls, resultados, erros, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.start_urls = urls
        self.resultados = resultados
        self.erros = erros


    def parse(self, response):

        if response.status != 200:

            self.erros.append(
                f"{response.url} (HTTP {response.status})"
            )

            return

        paragrafos = response.css(
            "p::text"
        ).getall()

        texto = " ".join(
            paragrafo.strip()
            for paragrafo in paragrafos
            if paragrafo.strip()
        )

        if texto:
            self.resultados.append(texto)


@crochet.wait_for(timeout=60)
def executar_crawler(urls, resultados, erros):

    runner = CrawlerRunner()

    return runner.crawl(
        PaginasWikipedia,
        urls=urls,
        resultados=resultados,
        erros=erros
    )


def coletar_paginas(assuntos):

    inicio = time.perf_counter()

    urls = [
        criar_url(assunto)
        for assunto in assuntos
    ]

    resultados = []
    erros = []

    try:

        executar_crawler(
            urls,
            resultados,
            erros
        )

    except Exception as erro:

        erros.append(
            f"Erro no Scrapy: {erro}"
        )

    duracao = time.perf_counter() - inicio

    return (
        " ".join(resultados),
        duracao,
        erros
    )