"""
main.py
Beschreibung: Hauptprogramm zur Verarbeitung von Geschwindigkeitsdaten aus einer JSON Datei.
Autoren: Martin Stoyanov und David Weber
Version: 1.0
"""
import pandas as pd
from utils import read_json, process_data

def main():
    """
    Hauptfunktion zur Ausführung des Programms.
    Liest die Daten aus einer JSON Datei, verarbeitet sie und gibt die Ergebnisse aus.
    """
    # Datei path definieren und daten einlesen
    file_path = "data/messungen.json"
    data = read_json(file_path)

    # daten verarbeiten
    processed_data = process_data(data)
    
    # pandas einstellungen für die Ausgabe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 100)
    
    # Ergebnisse ausgeben
    for label, df in processed_data.items():
        print(f"\n{label}:")
        print("=" * len(label))
        if isinstance(df, pd.DataFrame):
            print(df.to_string(index=True))
        elif isinstance(df, pd.Series):
            print(df.to_frame().to_string(index=True))
        else:
            print(df)

# programm automatisch ausführen
if __name__ == "__main__":
    main()