# operations.py
import os
import pandas as pd

from database_utils import  save_to_database, insert_into_disconnections_primary, insert_new_csv_to_database, decryption  
from hashing_utils import read_csv_file, hash_column, save_csv
from statistical_analysis import perform_statistical_analysis   
from  db_connection_string import connection_string

table_name_to_send = None # Global for opt3

def opt1():
    global table_name_to_send
    print("Hash, export files & store to database")
    directory_path = input("Enter the directory path: ").strip()
    file_name = input("Enter the file name (without extension): ").strip()
    extension = input("Enter the file extension: ").strip()

    path = os.path.join(directory_path, f"{file_name}.{extension}")

    column_to_hash = 'Λογαρ.Σύμβασ.'

    print('Start processing...')

    try:
        dfs = read_csv_file(path)
        print('Read File Completed')
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    dataf_hashed = hash_column(dfs, column_to_hash)
    dataf_combined = pd.concat([dataf_hashed, dfs], axis=1)

    print('Hash Completed')

    output_file_to_keep = os.path.join(directory_path, f"{file_name}_Hashed_toKeep.{extension}")
    output_file_to_send = os.path.join(directory_path, f"{file_name}_Hashed_toSend.{extension}")

    print('Generating Files')

    try:
        save_csv(dataf_combined, output_file_to_keep, encoding="utf-8")
        print(f'File with hashed column saved as {output_file_to_keep}')

        dataf_to_send = dataf_combined.drop(columns=[column_to_hash])
        save_csv(dataf_to_send, output_file_to_send, encoding="utf-8")
        print(f'File without original column saved as {output_file_to_send}')

    except Exception as e:
        print(f"Error saving files: {e}")
        return

    print('Process Completed...')
    print('Inserting the hashed file to the database')
    table_name_to_send = os.path.splitext(os.path.basename(output_file_to_keep))[0]
    save_to_database(dataf_combined, table_name_to_send, connection_string)

def opt2():
    print('Performing Statistical Analysis...')
    perform_statistical_analysis()

def opt3():
    print('Inserting to Disconections_Primary Table ')
    global table_name_to_send
    if table_name_to_send:
        insert_into_disconnections_primary(table_name_to_send, connection_string)
    else:
        print("No table name available. Please run option 1 first.")

def opt4():
    print("Inserting a new file to the database for Decryption ")
    table_name, directory_path = insert_new_csv_to_database(connection_string)
    decryption(table_name, connection_string, directory_path)
