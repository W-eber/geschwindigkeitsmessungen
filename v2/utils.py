"""
utils.py
Beschreibung: Hilfsfunktionen für die Verarbeitung von Geschwindigkeitsdaten aus einer JSON Datei mit funktionaler Programmierung.
Autoren: Martin Stoyanov und David Weber
Version: 2.0
"""

import pandas as pd
import json
from functools import reduce

def read_json(file_path):
    """
    Liest eine JSON Datei ein und gibt die Daten zurück.

    :param file_path: Pfad zur JSON Datei.
    :return: Die geladenen Daten als Dictionary.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def process_data(data):
    """
    Verarbeitet die Geschwindigkeitsdaten und gibt statistische Ergebnisse zurück.

    :param data: Die zu verarbeitenden Daten als Liste von Dictionaries.
    :return: Ein dictionary mit verschiedenen Statistiken über die Geschwindigkeitsdaten.
    """
    df = pd.DataFrame(data)
    
    df['hour'] = pd.to_datetime(df['messung_zeit'], format='%H:%M:%S').dt.hour
    df['month'] = pd.to_datetime(df['messung_datum']).dt.month
    df['day'] = pd.to_datetime(df['messung_datum']).dt.day

    # 1. schnellste / langsamste Einfahrtsgeschwindigkeit pro Monat
    speed_stats = (
        df.groupby('month')['v_einfahrt']
        .agg([('Min_Geschwindigkeit', 'min'), ('Max_Geschwindigkeit', 'max')])
        .reindex(range(1, 13), fill_value=0)
    )

    # 2. Anzahl der Überschreitungen der 30er Zone pro Monat (functional)
    monthly_exceedances = (
        df.pipe(lambda d: d[list(map(lambda v: v > 30, d['v_einfahrt']))])
        .groupby('month').size()
        .reindex(range(1, 13), fill_value=0)
        .reset_index(name='amount')
    )

    # 3. Durchschnittsgeschwindigkeit pro Stunde am Tag (functional)
    hourly_avg_speed = (df.groupby('hour')['v_einfahrt'].apply(lambda x: round(reduce(lambda a, b: a + b, x) / len(x))).reset_index(name='Durchschnittsgeschwindigkeit'))

    # 4. Anzahl der Überschreitungen in verschiedenen Kategorien pro Tag (functional)
    categorize_speed_exceedance = lambda delta: next(filter(lambda x: x[0](delta), [
        (lambda d: 1 <= d <= 5, '1-5 km/h'),
        (lambda d: 6 <= d <= 10, '6-10 km/h'),
        (lambda d: 11 <= d <= 15, '11-15 km/h'),
        (lambda d: 16 <= d <= 20, '15-20 km/h'),
        (lambda d: 21 <= d <= 25, '21-25 km/h'),
        (lambda d: d > 25, '25+ km/h'),
        (lambda d: True, '0 km/h')
    ]))[1]

    df['ueberschreitungs_kategorie'] = list(map(lambda v: categorize_speed_exceedance(v - 30), df['v_einfahrt']))
    daily_exceedance_categories = (df.pipe(lambda d: d[list(map(lambda x: x != '0 km/h', d['ueberschreitungs_kategorie']))]).groupby(['day', 'ueberschreitungs_kategorie']).size().unstack(fill_value=0).reindex(columns=['1-5 km/h', '6-10 km/h', '11-15 km/h', '15-20 km/h', '21-25 km/h', '25+ km/h'], fill_value=0))

    # 5. Differenz in der Anzahl Fahrzeuge, die beschleunigt oder gebremst haben (functional)
    df['verhalten'] = list(map(lambda v: 'beschleunigt' if v > 0 else 'gebremst', df['v_delta']))
    acceleration_braking_stats = (df.pivot_table(index='v_einfahrt', columns='verhalten', aggfunc='size', fill_value=0))

    return {
        "Schnellste/langsamste Einfahrtsgeschwindigkeit pro Monat": speed_stats,
        "Überschreitungen der 30er Zone pro Monat": monthly_exceedances,
        "Durchschnittsgeschwindigkeit pro Stunde am Tag": hourly_avg_speed,
        "Überschreitungen Kategorien pro Tag": daily_exceedance_categories,
        "Beschleunigt/Gebremst": acceleration_braking_stats
    }