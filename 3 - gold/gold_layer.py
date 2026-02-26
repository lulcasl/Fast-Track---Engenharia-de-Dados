import pandas as pd
import json
import os

# ====================================================================
# Etapa 1: Ler o arquivo criado na camada silver
# ====================================================================

# Definir o arquivo criado na camada anterior.
silver_file_path = '2 - silver/silver_issues.json'

# Ler o arquivo. Como coloquei o lines na bronze, preciso chamar aqui.
df_gold = pd.read_json(silver_file_path, lines=True)

print("=== GENERAL DATA ===")
print(df_gold.head(), "\n")
df_gold.info()
print("\n", f"Lines Total: {len(df_gold)}")
print(f"Column Total: {len(df_gold.columns)}", "\n")

# ====================================================================
# Etapa 2: Filtrar apenas os issues Done e Resolved
# ====================================================================

df_gold = df_gold[df_gold['issue_status'].isin(['Done', 'Resolved'])]
df_gold = df_gold.reset_index(drop=True)

print("=== AFTER FILTERING ===")
print(f"Total records after filter: {len(df_gold)}")
print("\nStatus distribution:")
print(df_gold['issue_status'].value_counts())
print("\nPriority distribution:")
print(df_gold['issue_priority'].value_counts())
print()