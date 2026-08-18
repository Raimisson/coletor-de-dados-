import os

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

CSV_ENTRADA = os.path.join("dados", "repositorio_unificado.csv")


def carregar_dados():
    return pd.read_csv(CSV_ENTRADA)


def preparar_features_e_alvo(df):
    df["bem_avaliado"] = (df["avaliacao"] >= 4).astype(int)

    disponivel_one_hot = pd.get_dummies(df["disponivel"], prefix="disponivel")

    X = pd.concat([df[["preco_brl"]], disponivel_one_hot], axis=1)
    y = df["bem_avaliado"]

    return X, y


def treinar_e_avaliar(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    acuracia = accuracy_score(y_test, y_pred)
    matriz_confusao = confusion_matrix(y_test, y_pred)

    print(f"Acurácia no teste: {acuracia:.4f}")
    print("Matriz de confusão:")
    print(matriz_confusao)


def main():
    df = carregar_dados()
    X, y = preparar_features_e_alvo(df)
    treinar_e_avaliar(X, y)


if __name__ == "__main__":
    main()
