import pandas as pd
import numpy as np
import os

# Load the loan dataset
df = pd.read_csv('output_files/loan_detail.csv')

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

# 4. Convert date columns to datetime if present
date_cols = [col for col in df.columns if 'date' in col.lower()]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# 5. Standardize common categorical columns
if 'gender' in df.columns:
    df['gender'] = df['gender'].str.strip().str.title()
    df['gender'] = df['gender'].replace({'M': 'Male', 'F': 'Female'})

if 'loan_status' in df.columns:
    df['loan_status'] = df['loan_status'].str.strip().str.title()

if 'loan_type' in df.columns:
    df['loan_type'] = df['loan_type'].str.strip().str.title()

# 6. Outlier detection and removal (using IQR) for loan amount
if 'loan_amount' in df.columns:
    Q1 = df['loan_amount'].quantile(0.25)
    Q3 = df['loan_amount'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df['loan_amount'] >= Q1 - 1.5 * IQR) & (df['loan_amount'] <= Q3 + 1.5 * IQR)]

# 7. Strip extra spaces from all string columns
for col in cat_cols:
    df[col] = df[col].str.strip()

# 8. Reset index after cleaning
df.reset_index(drop=True, inplace=True)

# 9. Save cleaned data to a different folder
output_folder = 'cleaned_data'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'loan_detail_cleaned.csv')
df.to_csv(output_file, index=False)

print(f"\n✅ Cleaned data saved to: {output_file}")

# 10. Show final cleaned data sample
print("\nCleaned Data Sample:")
print(df.head())
