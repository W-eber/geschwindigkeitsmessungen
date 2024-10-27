import pandas as pd
import json

def read_json(file_path):
    # JSON-Datei einlesen
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def process_data(data):
    # Daten in DataFrame umwandeln
    df = pd.DataFrame(data)
    # Stunde, Monat und Tag extrahieren
    df['hour'] = pd.to_datetime(df['messung_zeit'], format='%H:%M:%S').dt.hour
    df['month'] = pd.to_datetime(df['messung_datum']).dt.month
    df['day'] = pd.to_datetime(df['messung_datum']).dt.day
    return df