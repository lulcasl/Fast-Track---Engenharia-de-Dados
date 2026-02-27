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

# ====================================================================
# Etapa 3: Cálculo de tempo de resolução (horas)
# ====================================================================

# Calcula a diferença das colunas e converte os segundos em horas.
df_gold['resolution_time_hours'] = (df_gold['timestamp_updated_at'] - df_gold['timestamp_created_at']).dt.total_seconds() / 3600

# Checagem
print("=== RESOLUTION TIME CALCULATED ===")
print("Resolution time statistics:")
print(df_gold['resolution_time_hours'].describe())
print()

print("Sample data:")
print(df_gold[['issue_id', 'issue_priority', 'timestamp_created_at', 'timestamp_updated_at', 'resolution_time_hours']].head(10))

# Mapeamento das prioridades com base nas regras definidas.
map_priority_sla = {
    'High': 24,
    'Medium': 72,
    'Low': 120
}

#  Criando a nova coluna chamada 'sla_expected_hours'.
df_gold['sla_expected_hours'] = df_gold['issue_priority'].map(map_priority_sla)

print("=== SLA EXPECTED HOURS CALCULATED ===")
print("SLA expected hours statistics:")
print(df_gold['sla_expected_hours'].describe())
print()

df_gold['is_sla_met'] = df_gold['resolution_time_hours'] <= df_gold['sla_expected_hours']

print("=== SLA MET CALCULATED ===")
print("SLA met distribution:")
print(df_gold['is_sla_met'].value_counts())
print()