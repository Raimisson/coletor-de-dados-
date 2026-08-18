import csv
import os
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
PAGINAS = 5
INTERVALO_SEGUNDOS = 1
PASTA_SAIDA = "dados"
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "livros.csv")

RATING_TEXTO_PARA_NUMERO = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def extrair_avaliacao(article):
    tag_rating = article.find("p", class_="star-rating")
    if not tag_rating:
        return None
    classes = tag_rating.get("class", [])
    for classe in classes:
        if classe in RATING_TEXTO_PARA_NUMERO:
            return RATING_TEXTO_PARA_NUMERO[classe]
    return None


def extrair_disponibilidade(article):
    tag_estoque = article.find("p", class_="instock")
    if not tag_estoque:
        return None
    texto = tag_estoque.get_text(strip=True)
    return "In stock" in texto


def extrair_livros(html):
    soup = BeautifulSoup(html, "html.parser")
    livros = []
    for article in soup.find_all("article", class_="product_pod"):
        titulo = article.h3.a["title"]
        preco = article.find("p", class_="price_color").get_text(strip=True)
        avaliacao = extrair_avaliacao(article)
        disponivel = extrair_disponibilidade(article)
        livros.append(
            {
                "titulo": titulo,
                "preco": preco,
                "avaliacao": avaliacao,
                "disponivel": disponivel,
            }
        )
    return livros


def coletar_todos_os_livros():
    todos_os_livros = []
    for pagina in range(1, PAGINAS + 1):
        url = BASE_URL.format(pagina)
        print(f"Coletando página {pagina}: {url}")
        try:
            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()
            resposta.encoding = "utf-8"
        except requests.RequestException as erro:
            print(f"Falha ao acessar {url}: {erro}")
            continue

        livros_da_pagina = extrair_livros(resposta.text)
        todos_os_livros.extend(livros_da_pagina)
        print(f"  {len(livros_da_pagina)} livros encontrados")

        if pagina < PAGINAS:
            time.sleep(INTERVALO_SEGUNDOS)

    return todos_os_livros


def salvar_csv(livros):
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as arquivo_csv:
        campos = ["titulo", "preco", "avaliacao", "disponivel"]
        escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(livros)
    print(f"{len(livros)} livros salvos em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    livros = coletar_todos_os_livros()
    salvar_csv(livros)
