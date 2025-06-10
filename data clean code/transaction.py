import pandas as pd

# Define file path
csv_file = "transaction.csv"
cleaned_file = "cleaned_data/cleaned_customer_transaction.csv"

def clean_data(csv_file, cleaned_file):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Drop unnamed columns (if any)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Handle missing values
    df = df.dropna()  # Remove rows with null values
    # Alternatively, fill missing values: df.fillna(method='ffill', inplace=True)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Trim extra spaces from column names and values
    df.columns = df.columns.str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Convert data types (Example: Convert amount column to float if exists)
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Save cleaned data
    df.to_csv(cleaned_file, index=False)
    print("Data cleaned and saved successfully!")

# Execute the function
clean_data(csv_file, cleaned_file)