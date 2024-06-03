# hashing_utils.py
import pandas as pd
import hashlib

def hash_data(data):
    # Create a SHA-256 hash object
    sha_signature = hashlib.sha256()
    sha_signature.update(data.encode('utf-8'))
    return sha_signature.hexdigest()

def read_csv_file(path):
    return pd.read_csv(path, sep=';', encoding='greek', converters={'Λογαρ.Σύμβασ.': str, 'Εγγρ.αποσύνδεσ.': str})

def hash_column(dataf, column_name):
    dataf_hashed = dataf[[column_name]].astype(str).map(hash_data)
    dataf_hashed.rename(columns={column_name: f'Hashed {column_name}'}, inplace=True)
    return dataf_hashed

def save_csv(dataf, path, encoding, sep = ';'):
    dataf.to_csv(path, encoding="greek", sep=sep, index=False, na_rep='')