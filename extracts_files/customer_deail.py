import sqlite3
import pandas as pd
import os

# Step 1: Connect to SQLite and fetch data
sqlite_file = 'bank_data_base.db'  # Path to your SQLite file
table_name = 'customer_detail'    # Table name you want to export

conn = sqlite3.connect(sqlite_file)
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
conn.close()

# Step 2: Save as CSV in a specific folder
output_folder = 'output_files'  # Example folder name (you can change it)
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

csv_file = os.path.join(output_folder, 'customer_detail.csv')
df.to_csv(csv_file, index=False)
print(f"CSV file created at: {csv_file}")
