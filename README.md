# Coletor de Dados

Projeto de estudo de web scraping e unificação de dados em Python.

## O que o projeto faz

1. **Coleta** (`coletor.py`) — faz scraping de 5 páginas do site de prática
   [books.toscrape.com](https://books.toscrape.com), extraindo título, preço,
   avaliação (1 a 5 estrelas) e disponibilidade em estoque de cada livro.
   O resultado é salvo em `dados/livros.csv`.

2. **Unificação** (`unificar.py`) — combina os dados coletados com um
   sistema de estoque fictício (`dados/estoque-livraria.xlsx`), simulando um
   cenário real de integração entre sistemas diferentes:
   - Lê `dados/livros.csv` e `dados/estoque-livraria.xlsx`
   - Busca a cotação atual de GBP para BRL na API pública do
     [Frankfurter](https://api.frankfurter.dev/v1/latest)
   - Cria a coluna `preco_brl`, convertendo o preço (originalmente em libras)
     para reais
   - Junta os dois conjuntos de dados pelo título do livro, trazendo a
     coluna `estoque`
   - Salva o resultado em `dados/repositorio_unificado.csv`
   - Ao final, imprime quantas linhas não encontraram correspondência no
     estoque (títulos cadastrados de forma diferente entre os dois sistemas)

3. **Análise exploratória** (`eda.py`) — analisa `dados/repositorio_unificado.csv`:
   - Imprime no terminal o resumo estatístico (`describe()`) da coluna
     `preco_brl` e a correlação entre `preco_brl` e `avaliacao`
   - Gera e salva em `graficos/` três imagens: histograma da distribuição
     de preços, gráfico de barras com a quantidade de livros por avaliação
     (1 a 5 estrelas) e gráfico de dispersão entre preço e avaliação

4. **Modelo de classificação** (`modelo.py`) — treina uma Regressão
   Logística (scikit-learn) para prever `bem_avaliado` (avaliação >= 4)
   a partir de `preco_brl` e da coluna `disponivel` (one-hot encoding).
   Imprime a acurácia e a matriz de confusão no teste (20% dos dados).
   > **Limitação conhecida**: `disponivel` é `True` para todos os livros
   > coletados, então essa feature não carrega informação nenhuma, e
   > `preco_brl` tem correlação quase nula com a avaliação (ver EDA). O
   > modelo atual apenas prevê a classe majoritária. Para um modelo com
   > sinal real, seria necessário extrair a categoria/gênero verdadeiro
   > do livro no scraping (`coletor.py`) e usá-la como feature.

5. **Painel interativo** (`painel.py`) — dashboard em Streamlit sobre
   `dados/repositorio_unificado.csv`, com filtros na barra lateral
   (categoria/avaliação e faixa de preço), cartões de métrica (quantidade
   de livros, preço médio, avaliação média), gráfico de barras de livros
   por categoria e tabela com os dados filtrados.

## Estrutura dos dados

| Arquivo | Origem | Conteúdo |
|---|---|---|
| `dados/livros.csv` | `coletor.py` | título, preço, avaliação, disponível |
| `dados/estoque-livraria.xlsx` | fictício | título, estoque |
| `dados/repositorio_unificado.csv` | `unificar.py` | título, preço, avaliação, disponível, preco_brl, estoque |
| `graficos/*.png` | `eda.py` | histograma de preços, barras por avaliação, dispersão preço x avaliação |

## Como executar

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar os scripts

```bash
python coletor.py
python unificar.py
python eda.py
python modelo.py
streamlit run painel.py
```
