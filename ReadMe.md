# Web Scraping na Wikipédia

Projeto desenvolvido para a disciplina de Ciência de Dados.

O objetivo do projeto é utilizar diferentes bibliotecas de Python para realizar **web scraping em páginas da Wikipédia**, coletar seus conteúdos e realizar um processamento dos textos obtidos.

O projeto possui duas soluções:

- Requests + BeautifulSoup
- Scrapy + Crochet

Ao final do processamento, o sistema gera uma **nuvem de palavras** e permite consultar quantas vezes uma determinada palavra aparece no conteúdo das cinco páginas analisadas.

---

## Funcionalidades

O sistema permite:

1. Informar cinco assuntos separados por vírgula;
2. Acessar as respectivas páginas da Wikipédia;
3. Extrair o conteúdo textual das páginas;
4. Unificar o conteúdo das cinco páginas;
5. Limpar o texto;
6. Remover stopwords em português;
7. Pesquisar uma palavra específica;
8. Contar quantas vezes a palavra aparece no conteúdo;
9. Gerar uma nuvem de palavras;
10. Medir o tempo de execução de cada solução;
11. Comparar as soluções utilizando Requests + BeautifulSoup e Scrapy.

---

## Tecnologias utilizadas

- Python
- Streamlit
- Requests
- BeautifulSoup
- Scrapy
- Crochet
- NLTK
- WordCloud
- Matplotlib
- Pillow

---

## Estrutura do projeto

```text
Projeto_Ciencia_de_dados/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── nuvem.png
│
├── scrapers/
│   ├── __init__.py
│   ├── requests_scraper.py
│   └── scrapy_scraper.py
│
└── utils/
    ├── __init__.py
    └── text_processing.py