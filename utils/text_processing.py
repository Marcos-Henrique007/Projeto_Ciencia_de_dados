import re

import nltk

from nltk.corpus import stopwords


def obter_stopwords():

    try:

        return set(
            stopwords.words("portuguese")
        )

    except LookupError:

        nltk.download(
            "stopwords",
            quiet=True
        )

        return set(
            stopwords.words("portuguese")
        )


def limpar_texto(texto):

    texto = texto.lower()

    texto = re.sub(
        r"[^\w\s]",
        "",
        texto,
        flags=re.UNICODE
    )

    return texto


def remover_stopwords(texto):

    stop_words = obter_stopwords()

    palavras = texto.split()

    palavras_validas = [
        palavra
        for palavra in palavras
        if palavra not in stop_words
    ]

    return " ".join(palavras_validas)


def contar_palavra(texto, palavra):

    palavra = limpar_texto(
        palavra.strip()
    )

    if not palavra:
        return 0

    palavras = texto.split()

    return palavras.count(palavra)