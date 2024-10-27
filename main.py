import pandas as pd
from utils import read_json, process_data

def main():
    # Dateipfad definieren und Daten einlesen
    file_path = "messungen.json"
    data = read_json(file_path)
    # Daten verarbeiten
    processed_data = process_data(data)

if __name__ == "__main__":
    main()