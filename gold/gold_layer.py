import sys
import pandas as pd
import json
import os
from calculate_sla import calculate_business_hours, get_holidays_for_date_range

# ====================================================================
# Etapa 1: Read the file in the silver layer
# ====================================================================

# Ler o arquivo. Como coloquei o lines na bronze, preciso chamar aqui.
df_gold = pd.read_json("silver/silver_issues.json", lines=True)

print("=== GENERAL DATA ===")
print(df_gold.head(), "\n")
df_gold.info()
print("\n", f"Lines Total: {len(df_gold)}")
print(f"Column Total: {len(df_gold.columns)}", "\n")

# ====================================================================
# Step 2: Filter only Done and Resolved issues
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
# Step 3: Calculate resolution time and SLA compliance
# ====================================================================

# Calculates the difference between dates and converts to hours, only in business hours
# Calculating row by row with apply
def calculate_business_hours_row(row): 
    return calculate_business_hours(    
        row['timestamp_created_at'], 
        row['timestamp_updated_at']
    )

df_gold['resolution_time_hours'] = df_gold.apply(calculate_business_hours_row, axis=1) 

# Check if the  calculation is correctly applied.
print("=== RESOLUTION TIME CALCULATED ===")
print("Resolution time statistics:")
print(df_gold['resolution_time_hours'].describe())
print()

print("Sample data:")
print(df_gold[['issue_id', 'issue_priority', 'timestamp_created_at', 'timestamp_updated_at', 'resolution_time_hours']].head(10))

# Mapping the expected SLA hours based on priority, as defined in the documentation.
map_priority_sla = {
    'High': 24,
    'Medium': 72,
    'Low': 120
}

#  Creating new row 'sla_expected_hours'.
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

print("=== SLA COMPLIANCE BY PRIORITY ===")

# Aggregating by priority
sla_by_priority = df_gold.groupby('issue_priority').agg({
    'is_sla_met': ['sum', 'count']
})

# Calculating percentage
sla_by_priority.columns = ['sla_met', 'total']
sla_by_priority['sla_compliance_rate'] = (sla_by_priority['sla_met'] / sla_by_priority['total'] * 100).round(2)

print(sla_by_priority)
print()

# ====================================================================
# Step 4: Select and reorder final columns
# ====================================================================

df_gold_final = df_gold[[
    'issue_id',
    'issue_type',
    'assignee_name',
    'issue_priority',
    'timestamp_created_at',
    'timestamp_updated_at',
    'resolution_time_hours',
    'sla_expected_hours',
    'is_sla_met'
]]

# Checking final structure of the Gold table before saving.
print("=== FINAL GOLD TABLE STRUCTURE ===")
print(f"Total records: {len(df_gold_final)}")
print(f"Total columns: {len(df_gold_final.columns)}")
print()

print("Columns:")
print(df_gold_final.columns.tolist())
print()

print("First 10 rows:")
print(df_gold_final.head(10))

# ====================================================================
# Step 5: Save Gold layer
# ====================================================================

# Save main Gold table
output_path = 'gold/gold_sla_issues.json'

df_gold_final.to_json(
    output_path,
    orient='records',
    lines=True,
    force_ascii=False,
    date_format='iso'  # Mantém formato ISO das datas
)

# Verify file was created
if os.path.exists(output_path):
    print(f"✅ Gold table saved successfully: {output_path}")
else:
    print("❌ Error saving file")
    
# ====================================================================
# Step 6: Generating both reports
# ====================================================================

print("\n=== GENERATING REPORTS ===")

# Report 1: SLA by Analyst
report_by_analyst = df_gold_final.groupby('assignee_name').agg({
    'issue_id': 'count',  # Conta quantos issues
    'resolution_time_hours': 'mean'  # Média do tempo de resolução
}).reset_index()

# Renomear colunas
report_by_analyst.columns = ['analyst', 'total_issues', 'avg_resolution_hours']

# Arredondar a média
report_by_analyst['avg_resolution_hours'] = report_by_analyst['avg_resolution_hours'].round(2)

# Ordenar por quantidade de issues (decrescente)
report_by_analyst = report_by_analyst.sort_values('total_issues', ascending=False)

print("Report 1: SLA by Analyst")
print(report_by_analyst.head(10))
print()

# Report 2: SLA by Issue Type
report_by_issue = df_gold_final.groupby('issue_type').agg({
    'issue_id': 'count',  # Conta quantos issues
    'resolution_time_hours': 'mean'  # Média do tempo de resolução
}).reset_index()

# Renomear colunas
report_by_issue.columns = ['issue_type', 'total_issues', 'avg_resolution_hours']

# Arredondar a média
report_by_issue['avg_resolution_hours'] = report_by_issue['avg_resolution_hours'].round(2)

# Ordenar por quantidade de issues (decrescente)
report_by_issue = report_by_issue.sort_values('total_issues', ascending=False)

print("Report 2: SLA by Issue Type")
print(report_by_issue.head(10))
print()

# ====================================================================
# Step 7: Save reports as CSV
# ====================================================================

print("=== SAVING REPORTS ===")

report_by_analyst.to_csv(
    'gold/gold_sla_by_analyst.csv',
    index=False,
    encoding='utf-8'
)

print("✅ Report saved: gold_sla_by_analyst.csv")

report_by_issue.to_csv(
    'gold/gold_sla_by_issue_type.csv',
    index=False,
    encoding='utf-8'
)

print("✅ Report saved: gold_sla_by_issue_type.csv")

print("\n ALL GOLD LAYER FILES CREATED SUCCESSFULLY! ")
print("\nFiles generated:")
print("  - gold_sla_issues.json (main table)")
print("  - gold_sla_by_analyst.csv (report)")
print("  - gold_sla_by_issue_type.csv (report)")