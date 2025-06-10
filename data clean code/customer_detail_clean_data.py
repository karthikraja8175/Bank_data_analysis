import pandas as pd
import numpy as np
import os

# Load the dataset
df = pd.read_csv('output_files/customer_detail.csv')

# 1. Check basic info
print("Initial Info:")
print(df.info())
print(df.head())

# 2. Remove duplicate records
df = df.drop_duplicates()

# 3. Handle missing values
# Fill numeric missing values with median
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Fill categorical missing values with mode
cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# 4. Convert dates to datetime
if 'account_open_date' in df.columns:
    df['account_open_date'] = pd.to_datetime(df['account_open_date'], errors='coerce')

# 5. Standardize categorical columns
# Example for Gender column
if 'gender' in df.columns:
    df['gender'] = df['gender'].str.strip().str.title()
    df['gender'] = df['gender'].replace({'M': 'Male', 'F': 'Female'})

# Example for Account Type
if 'account_type' in df.columns:
    df['account_type'] = df['account_type'].str.strip().str.title()

# 6. Outlier detection and removal (using IQR) for balance
if 'balance' in df.columns:
    Q1 = df['balance'].quantile(0.25)
    Q3 = df['balance'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['balance'] >= Q1 - 1.5 * IQR) & (df['balance'] <= Q3 + 1.5 * IQR)]

# 7. Strip extra spaces from all string columns
for col in cat_cols:
    df[col] = df[col].str.strip()

# 8. Reset index after cleaning
df.reset_index(drop=True, inplace=True)

# 9. Save cleaned data to a different folder
output_folder = 'cleaned_data'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'customer_detail_cleaned.csv')
df.to_csv(output_file, index=False)

print(f"\n✅ Cleaned data saved to: {output_file}")

# 10. Show final cleaned data sample
print("\nCleaned Data Sample:")
print(df.head())
