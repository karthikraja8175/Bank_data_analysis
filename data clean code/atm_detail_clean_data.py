import pandas as pd
import numpy as np
import os

# Load the ATM dataset
df = pd.read_csv('output_files/atm_detail.csv')

# 1. View dataset info
print("Initial Dataset Info:")
print(df.info())
print(df.head())

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Handle missing values
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
cat_cols = df.select_dtypes(include=['object']).columns

# Fill numeric columns with median
for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Fill categorical columns with mode
for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# 4. Convert dates if there are any date columns (example: 'installation_date')
if 'installation_date' in df.columns:
    df['installation_date'] = pd.to_datetime(df['installation_date'], errors='coerce')

# 5. Standardize categorical columns
for col in cat_cols:
    df[col] = df[col].str.strip().str.title()

# Example: if there is a 'status' column (e.g., Active/Inactive/active)
if 'status' in df.columns:
    df['status'] = df['status'].replace({'Active': 'Active', 'Inactive': 'Inactive', 'active': 'Active', 'inactive': 'Inactive'})

# 6. Handle outliers (e.g., ATM Cash Capacity, if available)
if 'cash_capacity' in df.columns:
    Q1 = df['cash_capacity'].quantile(0.25)
    Q3 = df['cash_capacity'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['cash_capacity'] >= Q1 - 1.5 * IQR) & (df['cash_capacity'] <= Q3 + 1.5 * IQR)]

# 7. Reset index
df.reset_index(drop=True, inplace=True)

# 8. Save cleaned data to a custom folder
output_folder = 'cleaned_data'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'atm_detail_cleaned.csv')
df.to_csv(output_file, index=False)

print(f"\n✅ Cleaned data saved to: {output_file}")

# 9. Display sample cleaned data
print("\nCleaned ATM Data Sample:")
print(df.head())
