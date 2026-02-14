import pandas as pd
import json
import os

# Ler o JSON na camada bronze.
# Entender melhor o with [!]
with open('jira_issues_raw.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Criando o dataframe para ser referenciado posteriormente.
df_bronze = pd.DataFrame(data['issues'])

# Verifica o tipo do conteúdo que temos no JSON.
print("=== 🐼  PROJECT ===")
print(type(data['project']))
print(data['project'], "\n")

# Verificar o conteúdo de 'issues'.
print("=== 🐼  ISSUES ===")
print(type(data['issues']), "\n")
# Função f converte automaticamente todos os dados para string.

# Verificar as colunas existentes.
print("=== 🐼  COLUNAS ===")
print(df_bronze.columns.tolist(), "\n")

# Trazer algumas informações gerais com a função info() do pandas.
print("=== 🐼  INFORMAÇÕES ===")
print(df_bronze.info(), "\n")

# Verificar o conteúdo dos cinco primeiros registros.
print("=== 🐼 CONTEÚDO ===")
print(df_bronze.head(5), "\n")


# ===================================================================
# Até aqui foram todos os dadods sobre issues, preciso trazer tudo
# que esteja relacionado a parte de projetos também
# ===================================================================