#database_utils.py
import pyodbc
import os
import pandas as pd
import csv

from hashing_utils import read_csv_file

def save_to_database(df, table_name, connection_string):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        df = df.iloc[:, :2]
        df.columns = ['Hashed_CA', 'CA']

        columns = ", ".join([f"{col} NVARCHAR(MAX)" for col in df.columns])
        create_table_query = f"""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
            CREATE TABLE {table_name} ({columns})
        """
        print('Saving to database...')
        cursor.execute(create_table_query)

        for index, row in df.iterrows():
            placeholders = ", ".join("?" * len(row))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        print(f'Data saved to table {table_name} in the database.')
    except Exception as e:
        print(f"Error saving data to database: {e}")
    finally:
        connection.close()

def insert_into_disconnections_primary(table_name_to_send, connection_string):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        insert_query = f"""
            INSERT INTO Disconections_Primary (Hashed_CA, CA)
            SELECT DISTINCT b.Hashed_CA, b.CA
            FROM {table_name_to_send} b
            LEFT JOIN Disconections_Primary a ON a.Hashed_CA = b.Hashed_CA
            WHERE a.Hashed_CA IS NULL;
        """
        print('Inserting...')
        cursor.execute(insert_query)
        connection.commit()
        print('Data inserted into Disconections_Primary.')

    except Exception as e:
        print(f"Error inserting data into Disconections_Primary: {e}")
    finally:
        connection.close()

def insert_new_csv_to_database(connection_string):
    directory_path = input("Enter the directory path of the new CSV file: ").strip()
    file_name = input("Enter the file name (without extension) of the new CSV file: ").strip()
    extension = input("Enter the file extension of the new CSV file: ").strip()

    path = os.path.join(directory_path, f"{file_name}.{extension}")

    try:
        df = read_csv_file(path)
        print('Read File Completed')
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    df = df.iloc[:, :2]
    df.columns = ['Hashed_CA', 'CA']

    table_name_to_send = os.path.splitext(os.path.basename(path))[0]

    save_to_database(df, table_name_to_send, connection_string)

    return table_name_to_send , directory_path

def decryption(table_name, connection_string, directory_path):
    output_file_name = input("Please enter the output file name (with .csv extension): ")
    output_file = os.path.join(directory_path, output_file_name)
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        query = f"""
            SELECT DISTINCT r.Hashed_CA, a.CA
            FROM {table_name} r
            LEFT JOIN Disconections_Primary a ON r.Hashed_CA = a.Hashed_CA
            ORDER BY r.Hashed_CA;
        """
        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(row)

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Hashed_CA', 'CA']) 
            for row in results:
                writer.writerow(row)
        print(f"Decryption results stored to file {output_file}")

    except Exception as e:
        print(f"Error running decryption query: {e}")
    finally:
        connection.close()