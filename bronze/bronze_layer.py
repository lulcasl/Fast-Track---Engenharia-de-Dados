import pandas as pd
import json
import os

# ====================================================================
# Step 1: Open the JSON file, setting relative path to file.
# ====================================================================

with open("bronze/jira_issues_raw.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ====================================================================
# Step 2: Creating the dataframe from the JSON file.
# ====================================================================

# Creating the dataframe.
df_bronze = pd.DataFrame(data["issues"])

print("=== INITIAL INFORMATION ===", "\n")

# Checking the content type of 'project'.
print("=== PROJECT ===")
print(type(data['project']))
print(data['project'], "\n")

# Checking the content type of 'issues'.
print("=== ISSUES ===")
print(type(data['issues']), "\n")

# Since issues is a list check the content type of the first row.
print("=== COLUMNS ===")
for col in df_bronze.columns:
    print(f"{col}: {type(df_bronze[col][0])}")

print("\n","=== CHECK ASSIGNEE LIST ===")
# Checking the type of 'assignee'
print("Types of 'assignee':")
print(type(df_bronze['assignee'][0]))
print(df_bronze['assignee'][0], "\n")

print("\n","=== CHECK TIMESTAMPS LIST ===")
# Checking the type of 'timestamps'
print("Types of 'timestamps':")
print(type(df_bronze['timestamps'][0]))
print(df_bronze['timestamps'][0], "\n")

# Calling general information from dataframe with info()
print("=== INFORMATIONS ===")
df_bronze.info()
print("\n")

# ===================================================================
# Step 3: Create new columns with data from 'project'.
# ===================================================================

# Create new column with data from 'project', directly referencing
# the columns from the file, as per the open dictionary above.
df_bronze['project_id'] = data['project']['project_id']
df_bronze['project_name'] = data['project']['project_name']
df_bronze['extracted_at'] = data['project']['extracted_at']

# ===================================================================
# Step 4: Generate timestamp from ingested_at.
# ===================================================================

# Friendly reminder for myself that ingest =/= exctract.
df_bronze['ingested_at'] = pd.Timestamp.now()

print("=== UPDATED CONTENT ===")
print(df_bronze.head(5), "\n")

# ===================================================================
# Step 5: Finishing the bronze layer.
# ===================================================================

# Saving the final dataframe in the bronze layer with a specific function
# from Pandas for JSON. Initially I thought about doing it with parquet, but
# even though parquet has gains, I would have to download other libraries
# which would go against the rules of the challenge.

df_bronze.to_json('bronze/bronze_issues.json', 
                  orient='records', 
                  lines=True, 
                  force_ascii=False)

# I decided to save as JSON with lines = true for three reasons:
# 1. Simplicity in reading the file;
# 2. Better performance;
# 3. Smaller file.

print("=== FINAL COLUMNS ===")
for col in df_bronze.columns:
    print(f"{col}: {type(df_bronze[col][0])}")
print("\n")

if os.path.exists('bronze/bronze_issues.json'):
    print("✅ File saved successfully!")
