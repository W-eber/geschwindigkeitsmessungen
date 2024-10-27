"""
utils.py
Beschreibung: Hilfsfunktionen zur Verarbeitung von Geschwindigkeitsdaten aus einer JSON Datei.
Autor: Martin Stoyanov und David Weber
Version: 1.0
"""
import pandas as pd
import json

def read_json(file_path):
    """
    Liest eine JSON Datei ein und gibt die enthaltenen Daten zurück.

    Parameter:
    file_path (str): Der Pfad zur JSON Datei.

    Rückgabewert:
    dict: Die Daten aus der JSON Datei.
    """
    # JSON Datei einlesen
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def process_data(data):
    """
    Verarbeitet die eingelesenen Daten und erstellt verschiedene Statistiken.

    Parameter:
    data (dict): Die eingelesenen Daten als Dictionary.

    Rückgabewert:
    dict: Ein Dictionary mit verschiedenen Statistiken.
    """
    # dataframe erstellen und in dataframe umwandeln
    df = pd.DataFrame(data)

    # Datum und Zeit konvertieren
    df['hour'] = pd.to_datetime(df['messung_zeit'], format='%H:%M:%S').dt.hour
    df['month'] = pd.to_datetime(df['messung_datum']).dt.month
    df['day'] = pd.to_datetime(df['messung_datum']).dt.day

    # 1. schnellste / langsamste Einfahrtsgeschwindigkeit pro Monat
    speed_stats = df.groupby('month')['v_einfahrt'].agg(
        Min_Geschwindigkeit='min',
        Max_Geschwindigkeit='max'
    ).reindex(range(1, 13), fill_value=0)

    # 2. Anzahl der Überschreitungen der 30er Zone pro Monat
    df['ueberschreitung_30'] = df['v_einfahrt'] > 30
    monthly_exceedances = (
        df[df['ueberschreitung_30']]
        .groupby('month')
        .size()
        .reindex(range(1, 13), fill_value=0)
    )
    monthly_exceedances.index = monthly_exceedances.index.map(lambda x: f"Monat {x}")
    monthly_exceedances.name = 'Überschreitungen > 30 km/h'

    # 3. Durchschnittsgeschwindigkeit pro Stunde am Tag
    hourly_avg_speed = df.groupby('hour')['v_einfahrt'].mean().round().astype(int).reset_index(name='Durchschnittsgeschwindigkeit')

    # 4. Anzahl der Überschreitungen in verschiedenen Kategorien pro Tag
    def categorize_speed_exceedance(row):
        delta = row['v_einfahrt'] - 30
        if 1 <= delta <= 5:
            return '1-5 km/h'
        elif 6 <= delta <= 10:
            return '6-10 km/h'
        elif 11 <= delta <= 15:
            return '11-15 km/h'
        elif 16 <= delta <= 20:
            return '15-20 km/h'
        elif 21 <= delta <= 25:
            return '21-25 km/h'
        elif delta > 25:
            return '25+ km/h'
        else:
            return '0 km/h'

    df['ueberschreitungs_kategorie'] = df.apply(categorize_speed_exceedance, axis=1)
    daily_exceedance_categories = df[df['ueberschreitungs_kategorie'] != '0 km/h'].groupby(['day', 'ueberschreitungs_kategorie']).size().unstack(fill_value=0)
    category_order = ['1-5 km/h', '6-10 km/h', '11-15 km/h', '15-20 km/h', '21-25 km/h', '25+ km/h']
    daily_exceedance_categories = daily_exceedance_categories[category_order]

    # 5. Differenz in der Anzahl Fahrzeuge, die beschleunigt oder gebremst haben
    df['verhalten'] = df.apply(
        lambda row: 'beschleunigt' if row['v_delta'] > 0 else 'gebremst', axis=1
    )
    acceleration_braking_stats = df.pivot_table(
        index='v_einfahrt', columns='verhalten', aggfunc='size', fill_value=0
    )

    return {
        "Schnellste/langsamste Einfahrtsgeschwindigkeit pro Monat": speed_stats,
        "Überschreitungen der 30er Zone pro Monat": monthly_exceedances,
        "Durchschnittsgeschwindigkeit pro Stunde am Tag": hourly_avg_speed,
        "Überschreitungen Kategorien pro Tag": daily_exceedance_categories,
        "Beschleunigt/Gebremst": acceleration_braking_stats
    }