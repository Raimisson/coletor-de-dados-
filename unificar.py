import csv
import os
import sys

import pandas as pd
import requests

CSV_LIVROS = os.path.join("dados", "livros.csv")
XLSX_ESTOQUE = os.path.join("dados", "estoque-livraria.xlsx")
CSV_SAIDA = os.path.join("dados", "repositorio_unificado.csv")

FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"


def buscar_cotacao_gbp_brl():
    resposta = requests.get(
        FRANKFURTER_URL, params={"base": "GBP", "symbols": "BRL"}, timeout=10
    )
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["rates"]["BRL"]


def preco_para_float(preco_texto):
    return float(preco_texto.replace("£", "").strip())


def unificar():
    livros = pd.read_csv(CSV_LIVROS)
    estoque = pd.read_excel(XLSX_ESTOQUE)

    try:
        taxa_gbp_brl = buscar_cotacao_gbp_brl()
    except requests.RequestException as erro:
        sys.exit(f"Erro ao buscar cotação GBP/BRL na API Frankfurter: {erro}")

    print(f"Cotação atual: 1 GBP = {taxa_gbp_brl:.4f} BRL")

    livros["preco_brl"] = (
        livros["preco"].apply(preco_para_float) * taxa_gbp_brl
    ).round(2)

    unificado = livros.merge(estoque, on="titulo", how="left")

    sem_correspondencia = unificado["estoque"].isna().sum()

    unificado.to_csv(CSV_SAIDA, index=False, encoding="utf-8")

    print(f"Arquivo salvo em {CSV_SAIDA} com {len(unificado)} linhas")
    print(f"Linhas sem correspondência no estoque: {sem_correspondencia}")


if __name__ == "__main__":
    unificar()
