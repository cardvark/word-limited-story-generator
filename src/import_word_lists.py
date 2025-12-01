import sqlite3
import pandas as pd
import os

# table_name = 'chinese_word_groups'

# def generate_database(csv_file_path, db_file_path, table_name):
#     if os.path.isfile(db_file_path):
#         print(f"Database {db_file_path} exists.")
#     else:
#         print(f"Creating new database at {db_file_path}.")
#     df = pd.read_csv(csv_file_path)
#     conn = sqlite3.connect(db_file)
    
#     df.to_sql(table_name, conn, if_exists='fail', index=False)

#     # return conn.cursor()

# def get_db_cursor(db_file_path, table_name):
#     # df = pd.read_csv(csv_file_path)
#     conn = sqlite3.connect(db_file_path)

#     return conn.cursor()
    

def get_db_cursor(csv_file_path, table_name):
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect(":memory:")
    
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    return conn.cursor()
