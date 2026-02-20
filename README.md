# Demand Management - Data Ingestion and Processing

## Project Overview
This project implements a data ingestion and processing pipeline for the BANA6390 Unit 2 Assignment on pricing optimization.

## Files Created

### 1. `data_ingestion.py`
**Purpose**: Ingestion layer for reading and validating Excel data

**Key Features**:
- `DataIngestion` class handles reading Excel files
- Supports reading individual sheets or all sheets
- Data validation and preview functionality
- Error handling for missing files

**Main Methods**:
- `load_excel()`: Load the Excel file
- `read_original_data()`: Read the main data sheet
- `read_sheet()`: Read any specific sheet
- `validate_data()`: Validate loaded data
- `preview_data()`: Display data preview

### 2. `process_data.py`
**Purpose**: Processing layer to convert raw Excel data into clean DataFrames

**Key Features**:
- `DataProcessor` class for data cleaning and transformation
- Converts case-level data to unit-level data
- Calculates key metrics (margins, market share, profits)
- Exports clean data to CSV

**Main Methods**:
- `load_and_clean_original_data()`: Load and clean raw data
- `calculate_unit_level_data()`: Calculate unit-level metrics
- `get_summary_statistics()`: Generate summary stats
- `export_to_csv()`: Export processed data

## Data Structure

### Input Data (from Excel)
- **Week**: Week number (1-104)
- **Private Label**:
  - Retail Price (per unit)
  - Cases Sold
  - Retailer Cost (per case)
- **Brand 1**:
  - Retail Price (per unit)
  - Cases Sold
  - Retailer Cost (per case)
  - Manufacturing Cost (per case)

### Processed Data (Output)
All original columns plus calculated fields:

**Unit Conversions** (24 units per case):
- Brand1_Units_Sold
- PrivateLabel_Units_Sold
- Brand1_Unit_Cost
- PrivateLabel_Unit_Cost
- Brand1_Mfg_Cost_Per_Unit

**Margin Calculations**:
- Brand1_Retail_Margin ($ per unit)
- PrivateLabel_Retail_Margin ($ per unit)
- Brand1_Margin_Pct (%)
- PrivateLabel_Margin_Pct (%)

**Market Metrics**:
- Total_Units_Sold
- Brand1_Share (%)
- PrivateLabel_Share (%)
- Price_Gap ($)

**Profit Calculations**:
- Retailer_Profit_Brand1
- Retailer_Profit_PL
- Retailer_Total_Profit
- Brand1_Mfg_Profit

## Summary Statistics (from processed data)

### 1. Average Retail Prices (per unit):
- **Brand 1**: $2.61
- **Private Label**: $2.15
- **Price Gap**: $0.46 (Brand 1 priced higher)

### 2. Average Retail Margins:
- **Brand 1**: 17.12%
- **Private Label**: 23.09%

### 3. Average Weekly Unit Sales:
- **Brand 1**: 3,221 units
- **Private Label**: 4,545 units

### 4. Average Market Share:
- **Brand 1**: 41.31%
- **Private Label**: 58.69%

### 5. Average Weekly Profits:
- **Retailer**: $3,688.52
- **Manufacturer (Brand 1)**: $1,801.69

## Usage

### Run Data Ingestion Only:
```python
from data_ingestion import DataIngestion

ingestion = DataIngestion('bana6390_u2_assignment.xlsx')
ingestion.load_excel()
df = ingestion.read_original_data()
```

### Run Complete Processing Pipeline:
```python
from process_data import DataProcessor

processor = DataProcessor('bana6390_u2_assignment.xlsx')
df_clean = processor.load_and_clean_original_data()
df_units = processor.calculate_unit_level_data(df_clean)
stats = processor.get_summary_statistics(df_units)
```

### Run from Command Line:
```bash
# Process data and export to CSV
python process_data.py
```

## Output Files

- **pricing_data_clean.csv**: Cleaned data with all calculated metrics

## Dependencies

```
pandas
openpyxl
numpy
```

## Notes

- 24 units per case (constant)
- Selling cost: $10.00 per case ($0.4167 per unit)
- Data covers 104 weeks
- Category consists of only these two brands
