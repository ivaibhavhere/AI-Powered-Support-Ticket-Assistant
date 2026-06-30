import pandas as pd
import sqlite3
import os

DB_PATH = "tickets.db"
CSV_PATH = "support_tickets.csv"

def ingest_data():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return False
        
    print(f"Loading data from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    
    # Optional: basic cleaning/preprocessing
    # Ensure datetimes are properly formatted as strings for SQLite
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
    # Connect to SQLite and write
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("tickets", conn, if_exists="replace", index=False)
    
    # Create indexes for performance
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON tickets(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON tickets(priority);")
    conn.commit()
    conn.close()
    
    print(f"Successfully ingested {len(df)} records into {DB_PATH}.")
    return True

if __name__ == "__main__":
    ingest_data()
