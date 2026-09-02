import re

import nltk

from nltk.corpus import stopwords


# Baixa as stopwords em português:

nltk.download(
    "stopwords",
    quiet=True
)


# Limpa o texto:

def limpar_texto(
    texto
):

    texto = texto.lower()

    texto = re.sub(
        r"[^\w\s]",
        "",
        texto
    )

    return texto


# Remove as stopwords:

def remover_stopwords(
    texto
):

    stop_words = set(
        stopwords.words(
            "portuguese"
        )
    )


    palavras = texto.split()


    palavras_validas = [

        palavra

        for palavra in palavras

        if palavra not in stop_words

    ]


    return " ".join(
        palavras_validas
    )


# Conta a quantidade de uma palavra:

def contar_palavra(
    texto,
    palavra
):

    palavra = limpar_texto(
        palavra
    )


    palavras = texto.split()


    return palavras.count(
        palavra
    )