import pandas as pd
import json
import os

# ====================================================================
# Etapa 1: Ler o arquivo criado na camada bronze
# ====================================================================

# Definir o arquivo criado na camada anterior.
bronze_file_path = '1 - bronze/bronze_issues.json'

# Ler o arquivo. Como coloquei o lines na bronze, preciso chamar aqui.
# Lembrar da PEP8 [!].
df_silver = pd.read_json(bronze_file_path, lines=True)

print("=== DADOS GERAIS ===")
print(df_silver.head(), "\n")
df_silver.info()
print("\n", f"Total de linhas: {len(df_silver)}")
print(f"Total de colunas: {len(df_silver.columns)}", "\n")

# ====================================================================
# Etapa 2: Normalizar todos os campos aninhados
# ====================================================================

# Verificar os dados existentes, pra poder normalizar os campos e unir
# posteriormente sem gerar confusão.
print("=== ASSIGNEE ===")
print(f"Tipo: {type(df_silver['assignee'][0])}")
print(f"Conteúdo: {df_silver['assignee'][0]}")
print(" === TIMESTAMPS === ")
print(f"Tipo: {type(df_silver['timestamps'][0])}")
print(f"Conteúdo: {df_silver['timestamps'][0]}", "\n")

# Normalizando os dados. Cada item da lista vira uma linha e cada campo
# vira uma coluna.
assignee_df = pd.json_normalize(df_silver['assignee'].explode())
timestamps_df = pd.json_normalize(df_silver['timestamps'].explode())
assignee_df.info()
timestamps_df.info()

# Renomear as colunas pra unir com os dados principais sem gerar confusão.
# Referenciar as colunas originais na camada bronze.
df_silver = df_silver.rename(columns={
    'id': 'issue_id',
    'status': 'issue_status',
    'priority': 'issue_priority',
    'assignee': 'issue_assignee',
    'timestamps': 'issue_timestamps',
    'project_id': 'issue_project_id',
    'project_name': 'issue_project_name',
    'extracted_at': 'issue_extracted_at',
    'ingested_at': 'issue_ingested_at'
})

assignee_df = assignee_df.rename(columns={
    'id': 'assignee_id',
    'name': 'assignee_name',
    'email': 'assignee_email'
})

timestamps_df = timestamps_df.rename(columns={
    'created_at': 'timestamp_created_at',
    'resolved_at': 'timestamp_updated_at'
})

# Alinhas os índices para unir os dados. Lembrando que o drop remove o índice
# original, para que eu possa criar um novo.
df_silver = df_silver.reset_index(drop=True)
assignee_df = assignee_df.reset_index(drop=True)
timestamps_df = timestamps_df.reset_index(drop=True)

# Unindo tudo. Nesse caso, o axis não é 0, igual costuma ser em outros
# contextos de primeira linha porque o axis 0 nesse caso é vertical.
# Ou seja, EMPILHARÍAMOS os dados.
df_silver = pd.concat([df_silver, assignee_df, timestamps_df], axis=1)

# Remover as colunas originais, agora que já estão normalizadas.
df_silver = df_silver.drop(columns=['issue_assignee'])
df_silver = df_silver.drop(columns=['issue_timestamps'])

# Conferindo o produto final.
print("=== DADOS GERAIS v2 ===")
print(df_silver.head(), "\n")
df_silver.info()
print("\n", f"Total de linhas: {len(df_silver)}")
print(f"Total de colunas: {len(df_silver.columns)}", "\n")

# ====================================================================
# Etapa 3: Ajustar a tipagem de dados
# ====================================================================

# errors = coerce transformar os erros em NaT (Nott a Time), que é o equivalente a NaN para datas
df_silver['timestamp_updated_at'] = pd.to_datetime(df_silver['timestamp_updated_at'], errors='coerce')
df_silver['timestamp_created_at'] = pd.to_datetime(df_silver['timestamp_created_at'], errors='coerce')

# Verificar tipos de dados após conversão
print("Tipos de dados das colunas de data:")
print(df_silver[['timestamp_created_at', 'timestamp_updated_at']].dtypes)
print()

# ====================================================================
# Etapa 4: Limpeza
# ====================================================================

# Verificar total ANTES da limpeza
print(f"Total de registros ANTES da limpeza: {len(df_silver)}")
print()

# Verificar total de NaT - sum() soma tudo que é True.
nat_created = df_silver['timestamp_created_at'].isna().sum()
nat_updated = df_silver['timestamp_updated_at'].isna().sum()

print(f"Total de registros com timestamp_created_at NaT: {nat_created}")
print(f"Total de registros com timestamp_updated_at NaT: {nat_updated}", '\n')

# Verificar issues resolvidos SEM data de resolução
resolved_issues_nat = df_silver['issue_status'].isin(['Done', 'Resolved']) & df_silver['timestamp_updated_at'].isna()

print(f"Total de issues resolvidos ou finalizados sem data de atualização: {resolved_issues_nat.sum()}")

df_silver = df_silver[df_silver['timestamp_created_at'].notna()]
df_silver = df_silver.reset_index(drop=True)
# Se ele foi done ou resolved, precisa ter uma data do update do card, do contrário é inconsistência.
resolved_issues_nat = df_silver['issue_status'].isin(['Done', 'Resolved']) & df_silver['timestamp_updated_at'].isna()
df_silver = df_silver[~resolved_issues_nat]
df_silver = df_silver.reset_index(drop=True)

# Verificar total DEPOIS da limpeza
print("\nStatus distribution after cleaning:")
print(df_silver['issue_status'].value_counts())
print()

# Verificar se ainda ficou algo inconsistente, se a primeira checagem já resolveu todos os problemas.
remaining_inconsistent = (df_silver['issue_status'].isin(['Done', 'Resolved']) & df_silver['timestamp_updated_at'].isna()).sum()
print(f"Remaining inconsistent records: {remaining_inconsistent}")

# Salva o arquivo final
df_silver.to_json('2 - silver/silver_issues.json', 
                  orient='records', 
                  lines=True, 
                  force_ascii=False)

if os.path.exists('2 - silver/silver_issues.json'):
    print("Arquivo salvo com sucesso!")