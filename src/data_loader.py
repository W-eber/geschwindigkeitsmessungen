import json
import pandas as pd

def lade_daten(dateipfad):
    with open(dateipfad, 'r', encoding='utf-8') as file:
        daten = json.load(file)
    return pd.DataFrame(daten)