import sqlite3
import pandas as pd


def get_db_cursor(csv_file_path, table_name):
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect(":memory:")
    
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    return conn.cursor()
