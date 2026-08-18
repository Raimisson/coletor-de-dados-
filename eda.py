import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CSV_ENTRADA = os.path.join("dados", "repositorio_unificado.csv")
PASTA_GRAFICOS = "graficos"

sns.set_theme(style="whitegrid")


def carregar_dados():
    return pd.read_csv(CSV_ENTRADA)


def imprimir_estatisticas(df):
    print("Resumo estatístico de preco_brl:")
    print(df["preco_brl"].describe())
    print()

    correlacao = df["preco_brl"].corr(df["avaliacao"])
    print(f"Correlação entre preco_brl e avaliacao: {correlacao:.4f}")


def gerar_histograma_precos(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df["preco_brl"], bins=20, kde=True, color="steelblue")
    plt.title("Distribuição de preços (R$)")
    plt.xlabel("Preço (R$)")
    plt.ylabel("Quantidade de livros")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PASTA_GRAFICOS, "histograma_precos.png"), dpi=150
    )
    plt.close()


def gerar_barras_livros_por_avaliacao(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(x="avaliacao", data=df, order=sorted(df["avaliacao"].unique()), color="steelblue")
    plt.title("Quantidade de livros por avaliação (estrelas)")
    plt.xlabel("Avaliação (estrelas)")
    plt.ylabel("Quantidade de livros")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PASTA_GRAFICOS, "livros_por_avaliacao.png"), dpi=150
    )
    plt.close()


def gerar_dispersao_preco_avaliacao(df):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="preco_brl", y="avaliacao", data=df, color="steelblue")
    plt.title("Dispersão entre preço e avaliação")
    plt.xlabel("Preço (R$)")
    plt.ylabel("Avaliação (estrelas)")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PASTA_GRAFICOS, "dispersao_preco_avaliacao.png"), dpi=150
    )
    plt.close()


def main():
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    df = carregar_dados()

    imprimir_estatisticas(df)

    gerar_histograma_precos(df)
    gerar_barras_livros_por_avaliacao(df)
    gerar_dispersao_preco_avaliacao(df)

    print(f"\nGráficos salvos na pasta {PASTA_GRAFICOS}/")


if __name__ == "__main__":
    main()
