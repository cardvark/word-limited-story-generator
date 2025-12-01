import sqlite3
import pandas as pd
import os

csv_file_path = "./data/character-table.csv"
db_file_path = "./data/characters_database.db"
table_name = 'chinese_word_groups'


def generate_database():
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect(db_file_path)
    
    df.to_sql(table_name, conn, if_exists='fail', index=False)

    conn.close()

def get_db_cursor():
    if not os.path.isfile(db_file_path):
        generate_database()
    conn = sqlite3.connect(db_file_path)

    return conn.cursor()
    