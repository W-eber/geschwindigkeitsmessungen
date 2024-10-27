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

    # schnellste / langsamste Einfahrtsgeschwindigkeit pro Monat berechnen
    speed_stats = df.groupby('month')['v_einfahrt'].agg(
        Min_Geschwindigkeit='min',
        Max_Geschwindigkeit='max'
    ).reindex(range(1, 13), fill_value=0)

    # Überschreitungen der 30er Zone pro Monat berechnen
    df['ueberschreitung_30'] = df['v_einfahrt'] > 30
    monthly_exceedances = (
        df[df['ueberschreitung_30']]
        .groupby('month')
        .size()
        .reindex(range(1, 13), fill_value=0)
    )
    monthly_exceedances.index = monthly_exceedances.index.map(lambda x: f"Monat {x}")
    monthly_exceedances.name = 'Überschreitungen > 30 km/h'

    # Durchschnittsgeschwindigkeit pro Stunde am Tag berechnen
    hourly_avg_speed = df.groupby('hour')['v_einfahrt'].mean().round().astype(int).reset_index(name='Durchschnittsgeschwindigkeit')

    return {
        "Schnellste/langsamste Einfahrtsgeschwindigkeit pro Monat": speed_stats,
        "Überschreitungen der 30er Zone pro Monat": monthly_exceedances,
        "Durchschnittsgeschwindigkeit pro Stunde am Tag": hourly_avg_speed
    }