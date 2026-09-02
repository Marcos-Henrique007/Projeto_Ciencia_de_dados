import time

import crochet

from scrapy import Spider, Request
from scrapy.crawler import CrawlerRunner

from urllib.parse import quote


# Inicializa o Crochet
crochet.setup()


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_URL = "https://pt.wikipedia.org/wiki/"


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0 Safari/537.36"
)


# ============================================================
# CRIA A URL DA PÁGINA
# ============================================================

def criar_url(assunto):

    nome_pagina = (
        assunto.strip()
        .replace(" ", "_")
    )

    return (
        BASE_URL
        + quote(nome_pagina)
    )


# ============================================================
# SPIDER
# ============================================================

class PaginasWikipedia(Spider):

    name = "paginas_wikipedia"

    custom_settings = {

        "USER_AGENT": USER_AGENT,

        "LOG_LEVEL": "ERROR",

        "DOWNLOAD_TIMEOUT": 15,

        "RETRY_ENABLED": True,

        "RETRY_TIMES": 2,

        "HTTPERROR_ALLOW_ALL": True,

        "CONCURRENT_REQUESTS": 5,

        "DOWNLOAD_DELAY": 0.2,

        "COOKIES_ENABLED": False,

        "ROBOTSTXT_OBEY": False

    }


    def __init__(
        self,
        assuntos,
        resultados,
        erros,
        progresso,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.assuntos = assuntos

        self.resultados = resultados

        self.erros = erros

        self.progresso = progresso


    # ========================================================
    # INICIA AS REQUISIÇÕES
    # ========================================================

    def start_requests(self):

        for indice, assunto in enumerate(
            self.assuntos,
            start=1
        ):

            url = criar_url(
                assunto
            )


            self.progresso.append(
                f"Processando página "
                f"{indice}/{len(self.assuntos)}: "
                f"{assunto}"
            )


            self.progresso.append(
                f"Pesquisando na Wikipédia: "
                f"{assunto}"
            )


            yield Request(

                url=url,

                callback=self.parse,

                errback=self.errback,

                meta={
                    "assunto": assunto,
                    "indice": indice
                },

                headers={
                    "User-Agent": USER_AGENT
                },

                dont_filter=True

            )


    # ========================================================
    # PROCESSA A RESPOSTA
    # ========================================================

    def parse(
        self,
        response
    ):

        assunto = response.meta.get(
            "assunto",
            response.url
        )


        indice = response.meta.get(
            "indice",
            "?"
        )


        # ----------------------------------------------------
        # VERIFICA O STATUS HTTP
        # ----------------------------------------------------

        if response.status == 404:

            mensagem = (
                f"Erro 404: a página "
                f"'{assunto}' não foi encontrada."
            )


            self.erros.append(
                mensagem
            )


            self.progresso.append(
                mensagem
            )


            return


        if response.status != 200:

            mensagem = (
                f"Erro HTTP {response.status}: "
                f"{assunto}"
            )


            self.erros.append(
                mensagem
            )


            self.progresso.append(
                mensagem
            )


            return


        # ----------------------------------------------------
        # PÁGINA ENCONTRADA
        # ----------------------------------------------------

        self.progresso.append(
            f"Página encontrada: {assunto}"
        )


        self.progresso.append(
            f"Acessando página: {response.url}"
        )


        # ----------------------------------------------------
        # LOCALIZA O CONTEÚDO PRINCIPAL DA WIKIPÉDIA
        # ----------------------------------------------------

        paragrafos = response.css(
            "#mw-content-text .mw-parser-output > p"
        )


        textos = []


        for paragrafo in paragrafos:

            texto = paragrafo.xpath(
                "string(.)"
            ).get()


            if texto:

                texto = " ".join(
                    texto.split()
                )


                if texto:

                    textos.append(
                        texto
                    )


        # ----------------------------------------------------
        # SEGUNDA TENTATIVA DE EXTRAÇÃO
        # ----------------------------------------------------
        #
        # Caso a estrutura da página seja diferente,
        # procura os parágrafos dentro do conteúdo principal.
        #

        if not textos:

            paragrafos = response.css(
                "#mw-content-text p"
            )


            for paragrafo in paragrafos:

                texto = paragrafo.xpath(
                    "string(.)"
                ).get()


                if texto:

                    texto = " ".join(
                        texto.split()
                    )


                    if texto:

                        textos.append(
                            texto
                        )


        # ----------------------------------------------------
        # JUNTA OS PARÁGRAFOS
        # ----------------------------------------------------

        texto_final = " ".join(
            textos
        )


        # ----------------------------------------------------
        # VERIFICA SE EXISTE CONTEÚDO
        # ----------------------------------------------------

        if texto_final:

            self.resultados.append(
                texto_final
            )


            self.progresso.append(
                f"Conteúdo extraído com sucesso: "
                f"{assunto}"
            )


        else:

            mensagem = (
                f"A página '{assunto}' "
                "foi encontrada, mas não possui "
                "conteúdo textual."
            )


            self.erros.append(
                mensagem
            )


            self.progresso.append(
                mensagem
            )


    # ========================================================
    # TRATA ERROS DE REQUISIÇÃO
    # ========================================================

    def errback(
        self,
        failure
    ):

        assunto = failure.request.meta.get(
            "assunto",
            failure.request.url
        )


        response = getattr(
            failure.value,
            "response",
            None
        )


        if response is not None:

            if response.status == 404:

                mensagem = (
                    f"Erro 404: a página "
                    f"'{assunto}' não foi encontrada."
                )


                self.erros.append(
                    mensagem
                )


                self.progresso.append(
                    mensagem
                )


                return


        mensagem = (
            f"Falha ao acessar '{assunto}': "
            f"{failure.value}"
        )


        self.erros.append(
            mensagem
        )


        self.progresso.append(
            f"Falha na requisição: {assunto}"
        )


# ============================================================
# EXECUTA O CRAWLER
# ============================================================

@crochet.run_in_reactor
def executar_crawler(
    assuntos,
    resultados,
    erros,
    progresso
):

    runner = CrawlerRunner({

        "USER_AGENT": USER_AGENT,

        "LOG_LEVEL": "ERROR",

        "DOWNLOAD_TIMEOUT": 15,

        "RETRY_ENABLED": True,

        "RETRY_TIMES": 2,

        "HTTPERROR_ALLOW_ALL": True

    })


    return runner.crawl(

        PaginasWikipedia,

        assuntos=assuntos,

        resultados=resultados,

        erros=erros,

        progresso=progresso

    )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def coletar_paginas(
    assuntos
):

    inicio = time.perf_counter()


    resultados = []

    erros = []

    progresso = []


    progresso.append(
        "Iniciando coleta com Scrapy..."
    )


    # --------------------------------------------------------
    # LIMPA OS ASSUNTOS
    # --------------------------------------------------------

    assuntos_validos = [

        assunto.strip()

        for assunto in assuntos

        if assunto and assunto.strip()

    ]


    if not assuntos_validos:

        erros.append(
            "Nenhum assunto foi informado."
        )


        duracao = (
            time.perf_counter()
            - inicio
        )


        return (
            "",
            duracao,
            erros,
            progresso
        )


    # --------------------------------------------------------
    # CRIA AS REQUISIÇÕES
    # --------------------------------------------------------

    try:

        tarefa = executar_crawler(

            assuntos_validos,

            resultados,

            erros,

            progresso

        )


        # Aguarda o Scrapy terminar.
        #
        # O Crochet cuida do reactor em uma thread
        # própria e evita que o Streamlit precise
        # controlar o reactor do Twisted.

        tarefa.wait(
            timeout=60
        )


    except Exception as erro:

        mensagem = (
            f"Erro no Scrapy: "
            f"{type(erro).__name__}: {erro}"
        )


        erros.append(
            mensagem
        )


    # --------------------------------------------------------
    # CALCULA O TEMPO
    # --------------------------------------------------------

    duracao = (
        time.perf_counter()
        - inicio
    )


    # --------------------------------------------------------
    # VERIFICA O RESULTADO
    # --------------------------------------------------------

    paginas_coletadas = len(
        resultados
    )


    total_paginas = len(
        assuntos_validos
    )


    if paginas_coletadas == total_paginas:

        progresso.append(
            f"Coleta finalizada: "
            f"{paginas_coletadas}/"
            f"{total_paginas} páginas "
            "extraídas com sucesso."
        )

    else:

        progresso.append(
            f"Coleta incompleta: "
            f"{paginas_coletadas}/"
            f"{total_paginas} páginas "
            "foram extraídas."
        )


    # --------------------------------------------------------
    # JUNTA TODO O TEXTO
    # --------------------------------------------------------

    conteudo = " ".join(
        resultados
    )


    # --------------------------------------------------------
    # RETORNO COMPATÍVEL COM O MAIN.PY
    # --------------------------------------------------------

    return (
        conteudo,
        duracao,
        erros,
        progresso
    )