import pandas as pd
import json
import os

# ====================================================================
# Step 1 1: Read the file created in the bronze
# ====================================================================

# Set the path to the file created in the previous layer.
bronze_file_path = 'bronze/bronze_issues.json'

# Read the file and store it in a dataframe.
df_silver = pd.read_json(bronze_file_path, lines=True)

print("=== GENERAL INFORMATION ===")
print(df_silver.head(), "\n")
df_silver.info()
print("\n", f"Line total: {len(df_silver)}")
print(f"Column total: {len(df_silver.columns)}", "\n")

# ====================================================================
# Step 2: Normalize all nested fields
# ====================================================================

# Check the content to normalize all data.
print("=== ASSIGNEE ===")
print(f"Tipo: {type(df_silver['assignee'][0])}")
print(f"Conteúdo: {df_silver['assignee'][0]}")
print(" === TIMESTAMPS === ")
print(f"Tipo: {type(df_silver['timestamps'][0])}")
print(f"Conteúdo: {df_silver['timestamps'][0]}", "\n")

# Normalizing data, each item in the list becomes a row and each field becomes a column.
assignee_df = pd.json_normalize(df_silver['assignee'].explode())
timestamps_df = pd.json_normalize(df_silver['timestamps'].explode())
assignee_df.info()
timestamps_df.info()

# Rename columns as set in the documentation.
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

# Align index to merge data. Remembering that drop removes the original index, so I can create a new one.
df_silver = df_silver.reset_index(drop=True)
assignee_df = assignee_df.reset_index(drop=True)
timestamps_df = timestamps_df.reset_index(drop=True)

# Merging everything. In this case, the axis is not 0, as it usually is
# in other contexts of the first line because axis 0 in this case is vertical.
# If that was the case, we would STACK the data.
df_silver = pd.concat([df_silver, assignee_df, timestamps_df], axis=1)

# Remove original columns that are no longer necessary.
df_silver = df_silver.drop(columns=['issue_assignee'])
df_silver = df_silver.drop(columns=['issue_timestamps'])

# Checking final data
print("=== GENERAL DATA ===")
print(df_silver.head(), "\n")
df_silver.info()
print("\n", f"Line total: {len(df_silver)}")
print(f"Column total: {len(df_silver.columns)}", "\n")

# ====================================================================
# Step 3: Set the correct data types for each column
# ====================================================================

# errors = coerce set errors to NaT (Nott a Time), equivalent to NaN for date values
df_silver['timestamp_updated_at'] = pd.to_datetime(df_silver['timestamp_updated_at'], errors='coerce')
df_silver['timestamp_created_at'] = pd.to_datetime(df_silver['timestamp_created_at'], errors='coerce')

# Check data types after conversion
print("Data type of date columns:")
print(df_silver[['timestamp_created_at', 'timestamp_updated_at']].dtypes)
print()

# ====================================================================
# Setp 4: Cleaning up
# ====================================================================

# Check totals before cleaning
print(f"Total of records BEFORE cleaning: {len(df_silver)}")
print()

# Check total of NaT - sum() soma tudo que é True.
nat_created = df_silver["timestamp_created_at"].isna().sum()
nat_updated = df_silver["timestamp_updated_at"].isna().sum()

print(f"Total of records with timestamp_created_at NaT: {nat_created}")
print(f"Total of records with timestamp_updated_at NaT: {nat_updated}", '\n')

# Check solved issues withoyut timestamp_updated_at
resolved_issues_nat = df_silver['issue_status'].isin(['Done', 'Resolved']) & df_silver['timestamp_updated_at'].isna()
print(f"Total of issues solved or finished WITHOUT timestamp_updated_at: {resolved_issues_nat.sum()}")

df_silver = df_silver[df_silver['timestamp_created_at'].notna()]
df_silver = df_silver.reset_index(drop=True)
# If the issue was done or resolved, it needs to have an update date, otherwise it's inconsistency.
resolved_issues_nat = df_silver['issue_status'].isin(['Done', 'Resolved']) & df_silver['timestamp_updated_at'].isna()
df_silver = df_silver[~resolved_issues_nat]
df_silver = df_silver.reset_index(drop=True)

# Check totals after cleaning
print("\nStatus distribution after cleaning:")
print(df_silver['issue_status'].value_counts())
print()

# Saving final file
df_silver.to_json('silver/silver_issues.json', 
                  orient='records', 
                  lines=True, 
                  force_ascii=False)

if os.path.exists('silver/silver_issues.json'):
    print("✅ File saved successfully!")