import os

import pandas as pd
import streamlit as st

CSV_ENTRADA = os.path.join("dados", "repositorio_unificado.csv")

st.set_page_config(page_title="Painel do Repositório Unificado", layout="wide")


@st.cache_data
def carregar_dados():
    return pd.read_csv(CSV_ENTRADA)


def main():
    st.title("Painel do Repositório Unificado")

    df = carregar_dados()

    st.sidebar.header("Filtros")

    categorias_disponiveis = sorted(df["avaliacao"].unique())
    categorias_selecionadas = st.sidebar.multiselect(
        "Categoria (avaliação em estrelas)",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
    )

    preco_min = float(df["preco_brl"].min())
    preco_max = float(df["preco_brl"].max())
    faixa_preco = st.sidebar.slider(
        "Faixa de preço (R$)",
        min_value=preco_min,
        max_value=preco_max,
        value=(preco_min, preco_max),
    )

    df_filtrado = df[
        df["avaliacao"].isin(categorias_selecionadas)
        & df["preco_brl"].between(faixa_preco[0], faixa_preco[1])
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("Quantidade de livros", len(df_filtrado))
    col2.metric(
        "Preço médio (R$)",
        f"{df_filtrado['preco_brl'].mean():.2f}" if len(df_filtrado) else "—",
    )
    col3.metric(
        "Avaliação média",
        f"{df_filtrado['avaliacao'].mean():.2f}" if len(df_filtrado) else "—",
    )

    st.subheader("Quantidade de livros por categoria (avaliação)")
    livros_por_categoria = (
        df_filtrado["avaliacao"].value_counts().sort_index()
    )
    st.bar_chart(livros_por_categoria)

    st.subheader("Dados filtrados")
    st.dataframe(df_filtrado)


if __name__ == "__main__":
    main()
