# Python Data Engineering Challenge – JIRA

A complete data engineering pipeline implementing the Medallion Architecture to process JIRA issues and calculate SLA metrics with business hours compliance.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [SLA Rules](#sla-rules)
- [Project Structure](#project-structure)
- [Output Files](#output-files)
- [Key Learnings](#key-learnings)

## 🎯 Overview

This project demonstrates a production-ready ETL pipeline that:
- Processes nested JSON data from JIRA
- Implements data quality checks and cleaning
- Calculates SLA metrics considering business hours, weekends, and Brazilian national holidays
- Generates analytical reports for business insights

## 🏗️ Architecture

The pipeline follows the **Medallion Architecture** pattern:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Bronze    │───▶│   Silver    │────▶│    Gold     │
│  Raw Data   │     │  Cleaned    │     │  Business   │
│             │     │  Normalized │     │   Metrics   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Bronze Layer
- Ingests raw JSON data from JIRA
- Minimal transformation
- Preserves nested structures
- Adds ingestion metadata

### Silver Layer
- Normalizes nested fields (assignee, timestamps)
- Converts data types (dates to datetime)
- Cleans invalid data
- Removes inconsistencies

### Gold Layer
- Filters resolved issues
- Calculates business hours resolution time
- Applies SLA rules by priority
- Generates analytical reports

## ✨ Features

- **Business Hours Calculation**: Accurately calculates working hours (9 AM - 5 PM)
- **Holiday Integration**: Fetches Brazilian national holidays via API
- **Weekend Exclusion**: Automatically excludes Saturdays and Sundays
- **Data Quality**: Validates and cleans inconsistent records
- **Modular Design**: Reusable SLA calculation functions
- **Multiple Outputs**: JSON for data, CSV for reports

## 📦 Requirements

- Python 3.11+
- pandas (only external library allowed for this challenge)

Standard library modules used:
- `json`
- `urllib`
- `datetime`
- `os`

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/python-data-engineering-challenge.git
cd python-data-engineering-challenge
```

2. Install dependencies:
```bash
pip install pandas
```

3. Ensure the raw data file exists at:
```
bronze/jira_issues_raw.json
```

## 💻 Usage

Run the pipeline in sequence:

```bash
# Step 1: Bronze layer (data ingestion)
python bronze/bronze_layer.py

# Step 2: Silver layer (data cleaning & normalization)
python silver/silver_layer.py

# Step 3: Gold layer (business metrics & reports)
python gold/gold_layer.py
```

### Testing SLA Functions

```bash
python gold/calculate_sla.py
```

## 🔄 Data Flow

```
jira_issues_raw.json (1000 issues)
    ↓
bronze_issues.json (1000 issues + metadata)
    ↓
silver_issues.json (990 issues - cleaned)
    ↓
gold_sla_issues.json (804 resolved issues)
    ↓
├── gold_sla_by_analyst.csv
└── gold_sla_by_issue_type.csv
```

## ⏱️ SLA Rules

| Priority | Expected Resolution Time |
|----------|-------------------------|
| High     | 24 business hours       |
| Medium   | 72 business hours       |
| Low      | 120 business hours      |

**Business Hours**: 9 AM - 5 PM (8 hours/day)
**Excluded Days**: Weekends and Brazilian national holidays

## 📁 Project Structure

```
.
├── bronze/
│   ├── bronze_layer.py           # Data ingestion script
│   ├── jira_issues_raw.json      # Raw input data
│   └── bronze_issues.json        # Output (generated)
│
├── silver/
│   ├── silver_layer.py           # Data cleaning script
│   └── silver_issues.json        # Output (generated)
│
├── gold/
│   ├── gold_layer.py             # Business metrics script
│   ├── calculate_sla.py          # SLA calculation functions
│   ├── gold_sla_issues.json      # Main table (generated)
│   ├── gold_sla_by_analyst.csv   # Report 1 (generated)
│   └── gold_sla_by_issue_type.csv # Report 2 (generated)
│
└── README.md
```

## 📊 Output Files

### Main Table: `gold_sla_issues.json`
Contains 804 resolved issues with:
- Issue ID, type, priority
- Assignee information
- Created and resolved timestamps
- Resolution time in business hours
- Expected SLA hours
- SLA compliance indicator

### Report 1: `gold_sla_by_analyst.csv`
Aggregated metrics per analyst:
- Analyst name
- Total issues resolved
- Average resolution time (hours)

### Report 2: `gold_sla_by_issue_type.csv`
Aggregated metrics per issue type:
- Issue type (Bug, Story, Task)
- Total issues resolved
- Average resolution time (hours)

## 🎓 Key Learnings

This project demonstrates:
- **ETL Pipeline Design**: Medallion architecture implementation
- **Data Quality**: Validation, cleaning, and consistency checks
- **Business Logic**: Complex SLA calculations with multiple constraints
- **API Integration**: External data source for holidays
- **Python Best Practices**: PEP 8, modular code, reusable functions
- **Data Engineering Concepts**: Incremental data processing, data lineage

## 📈 Results Summary

From the processed data:
- **1000** initial issues
- **990** after data quality checks
- **804** resolved issues analyzed
- **100%** SLA compliance rate
- **12.57 hours** average resolution time

## 🤝 Contributing

This is a learning project. Feedback and suggestions are welcome!

## 📄 License

This project is for educational purposes.

## 👤 Author

Lucas - Data Engineering Student

---

**Note**: This project was developed as a learning exercise to demonstrate data engineering skills including ETL pipeline design, data quality management, and business metric calculation.