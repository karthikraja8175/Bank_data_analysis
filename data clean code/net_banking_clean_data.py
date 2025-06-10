import pandas as pd
import numpy as np
import os

# Load the CSV file
df = pd.read_csv('output_files/net_banking.csv')  # adjust the path if needed

# 1. Check initial data info
print("Initial Data Info:")
print(df.info())
print(df.head())

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Handle missing values
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# 4. Convert any date columns (example: 'transaction_date')
for col in df.columns:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col], errors='coerce')

# 5. Standardize categorical data (example for 'status' and 'transaction_type')
if 'status' in df.columns:
    df['status'] = df['status'].str.strip().str.title()

if 'transaction_type' in df.columns:
    df['transaction_type'] = df['transaction_type'].str.strip().str.title()

# 6. Remove outliers using IQR method (example: 'transaction_amount')
if 'transaction_amount' in df.columns:
    Q1 = df['transaction_amount'].quantile(0.25)
    Q3 = df['transaction_amount'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['transaction_amount'] >= Q1 - 1.5 * IQR) & (df['transaction_amount'] <= Q3 + 1.5 * IQR)]

# 7. Strip all string columns to remove extra spaces
for col in cat_cols:
    df[col] = df[col].str.strip()

# 8. Reset index
df.reset_index(drop=True, inplace=True)

# 9. Save cleaned file
output_folder = 'cleaned_data'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'net_banking_cleaned.csv')
df.to_csv(output_file, index=False)

print(f"\n✅ Cleaned data saved to: {output_file}")

# 10. Show cleaned sample
print("\nCleaned Data Sample:")
print(df.head())
