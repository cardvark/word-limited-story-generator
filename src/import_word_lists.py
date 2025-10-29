import csv
import sqlite3
import pandas as pd

def get_word_groups_from_csv(csv_file_path):
    word_groups = {}

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        for row in csv_reader:
            group = row[3]
            word = row[0]
            # print(f"Found word: {word} in group: {group}")
            if group in word_groups:
                word_groups[group].append(word)
            else:
                word_groups[group] = [word]
                
    return word_groups


def get_sql_table_cursor(csv_file_path, table_name):
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect(":memory:")
    
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    return conn.cursor()
