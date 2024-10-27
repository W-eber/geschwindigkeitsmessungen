import pandas as pd
import json

def read_json(file_path):
    # JSON-Datei einlesen
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def process_data(data):
    pass