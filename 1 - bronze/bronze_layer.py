import pandas as pd
import json
import os

# ====================================================================
# Etapa 0: Abrir o JSON, definindo o caminho relativo do arquivo.
# ====================================================================

# Entender melhor o with [!]
with open("1 - bronze/jira_issues_raw.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ====================================================================
# Etapa 1: Criar um dataframe a partir do JSON.
# ====================================================================

# Criando o dataframe para ser referenciado posteriormente.
df_bronze = pd.DataFrame(data["issues"])

# Verifica o tipo do conteúdo que temos no JSON.
print("=== 🐼  PROJECT ===")
print(type(data['project']))
print(data['project'], "\n")

# Verificar o conteúdo de 'issues'.
print("=== 🐼  ISSUES ===")
print(type(data['issues']), "\n")
# Função f converte automaticamente todos os dados para string.

# Como issues é uma lista, verificar o tipo de dados da primeira linha.
print("=== 🐼  COLUNAS ===")
for col in df_bronze.columns:
    print(f"{col}: {type(df_bronze[col][0])}")
print("\n")

# Ver o tipo do primeiro valor de 'assignee'
print("Tipo de 'assignee':")
print(type(df_bronze['assignee'][0]))
print(df_bronze['assignee'][0], "\n")

# Ver o tipo do primeiro valor de 'timestamps'
print("Tipo de 'timestamps':")
print(type(df_bronze['timestamps'][0]))
print(df_bronze['timestamps'][0], "\n")

# Trazer algumas informações gerais com a função info() do pandas.
print("=== 🐼  INFORMAÇÕES ===")
print(df_bronze.info(), "\n")

# Verificar o conteúdo dos cinco primeiros registros.
print("=== 🐼 CONTEÚDO ===")
print(df_bronze.head(5), "\n")

# ===================================================================
# Etapa 2: Criar novas colunas com os dados de 'project'.
# ===================================================================

# Aqui, criar nova coluna com os dados de 'project', referenciado diretamente 
# as colunas do arquivo, conforme dicionário aberto anteriormente
df_bronze['project_id'] = data['project']['project_id']
df_bronze['project_name'] = data['project']['project_name']
df_bronze['extracted_at'] = data['project']['extracted_at']

# Verificar o conteúdo dos cinco primeiros registros com os novos dados.
print("=== 🐼 CONTEÚDO ATUALIZADO ===")
print(df_bronze.head(5), "\n")

# ===================================================================
# Etapa 3: Trazer um timestamp com os dados da extração.
# ===================================================================

# Lembrando que ingerir =/= extrair.
df_bronze['ingested_at'] = pd.Timestamp.now()

print("=== 🐼 CONTEÚDO ATUALIZADO v2 ===")
print(df_bronze.head(5), "\n")

# ===================================================================
# Etapa 4: Tratativa de campos aninhados.
# ===================================================================

# Na camada bronze, segundo a metodologia, os campos permanecem como
# listas, mantendo a estrutura original do JSON. A tratativa será feita
# na camada Silver.

# ===================================================================
# Etapa 5: Finalizando a camada bronze.
# ===================================================================

# Salvar o dataframe final na camada bronze com uma função específica
# do Pandas para JSON. Inicialmente pensei em fazer com parquet, mas
# apesar dos ganhos do parquet, eu teria que baixar outras bibliotecas
# o que iria contra as regras do desafio.

df_bronze.to_json('1 - bronze/bronze_issues.json', 
                  orient='records', 
                  lines=True, 
                  force_ascii=False)

# Decidi salvar como JSON com lines = true por três motivos:
# 1. Simplificdade na leitura do arquivo;
# 2. Melhor performance;
# 3. Arquivo menor.

# Por esses três motivos e um pouco pela maneira que prefiro ler
# e trabalhar com os dados, acho mais simples.

if os.path.exists('1 - bronze/bronze_issues.json'):
    print("✅ Arquivo salvo com sucesso!")
