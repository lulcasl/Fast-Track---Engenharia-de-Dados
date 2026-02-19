import pandas as pd
import json
import os

# ====================================================================
# Etapa 1: Ler o arquivo criado na camada bronze.
# ====================================================================

# Definir o arquivo criado na camada anterior.
bronze_file_path = '1 - bronze/bronze_issues.json'

# Ler o arquivo. Como coloquei o lines na bronze, precio por aqui.
# Lembrar da PEP8 [!].
df_silver = pd.read_json(bronze_file_path, lines=True)

print("=== 🐼 DADOS GERAIS ===")
print(df_silver.head(), "\n")
print(df_silver.info())
print(f"Total de linhas: {len(df_silver)}")
print(f"Total de colunas: {len(df_silver.columns)}")

# ====================================================================
# Etapa 2: Normalizar todos os campos aninhados.
# ====================================================================

# ====================================================================
# Etapa 3: Ajustar a tipagem de dados.
# ====================================================================

# ====================================================================
# Etapa 4: Limpeza.
# ====================================================================


