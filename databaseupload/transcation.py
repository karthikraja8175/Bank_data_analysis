import pandas as pd
import sqlite3

# Config
csv_file = 'transaction.csv'      # <-- replace with your CSV file name
sqlite_db = 'bank_data_base.db'
table_name = 'customer_transaction'

# Step 1: Read CSV
df = pd.read_csv(csv_file)

# Step 2: Connect to SQLite
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Step 3: Fix column quoting to handle spaces or keywords
columns = df.columns
col_types = ", ".join([f'"{col}" TEXT' for col in columns])  # <-- quoting columns using double quotes
cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({col_types});')

# Step 4: Insert Data
df.to_sql(table_name, conn, if_exists='append', index=False)

print("✅ CSV imported successfully without syntax errors!")

# Optional: Preview rows
for row in cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 5'):
    print(row)

conn.close()
