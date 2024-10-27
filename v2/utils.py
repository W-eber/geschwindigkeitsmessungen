import pandas as pd
import json

# JSON-Datei einlesen
def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def process_data(data):
    # dataframe erstellen und in dataframe umwandeln
    df = pd.DataFrame(data)
    
    # Datum und Zeit konvertieren
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
        df.assign(ueberschreitung_30=list(map(lambda v: v > 30, df['v_einfahrt'])))
        .pipe(lambda d: d[d['ueberschreitung_30']])
        .groupby('month').size()
        .reindex(range(1, 13), fill_value=0)
        .reset_index(name='amount')
    )

    # 3. Durchschnittsgeschwindigkeit pro Stunde am Tag (functional)
    hourly_avg_speed = (df.groupby('hour')['v_einfahrt'].apply(lambda x: round(x.mean())).reset_index(name='Durchschnittsgeschwindigkeit'))

    # 4. Anzahl der Überschreitungen in verschiedenen Kategorien pro Tag (functional)
    categorize_speed_exceedance = lambda delta: (
        '1-5 km/h' if 1 <= delta <= 5 else
        '6-10 km/h' if 6 <= delta <= 10 else
        '11-15 km/h' if 11 <= delta <= 15 else
        '15-20 km/h' if 16 <= delta <= 20 else
        '21-25 km/h' if 21 <= delta <= 25 else
        '25+ km/h' if delta > 25 else '0 km/h'
    )

    df['ueberschreitungs_kategorie'] = list(map(lambda v: categorize_speed_exceedance(v - 30), df['v_einfahrt']))
    daily_exceedance_categories = (
        df.pipe(lambda d: d[d['ueberschreitungs_kategorie'] != '0 km/h'])
        .groupby(['day', 'ueberschreitungs_kategorie']).size()
        .unstack(fill_value=0)
        .reindex(columns=['1-5 km/h', '6-10 km/h', '11-15 km/h', '15-20 km/h', '21-25 km/h', '25+ km/h'], fill_value=0)
    )

    # 5. Differenz in der Anzahl Fahrzeuge, die beschleunigt oder gebremst haben (functional)
    df['verhalten'] = list(map(lambda v: 'beschleunigt' if v > 0 else 'gebremst', df['v_delta']))
    acceleration_braking_stats = (
        df.pivot_table(index='v_einfahrt', columns='verhalten', aggfunc='size', fill_value=0)
    )

    # ergebnis als Dictionary zurückgeben
    return {
        "Schnellste/langsamste Einfahrtsgeschwindigkeit pro Monat": speed_stats,
        "Überschreitungen der 30er Zone pro Monat": monthly_exceedances,
        "Durchschnittsgeschwindigkeit pro Stunde am Tag": hourly_avg_speed,
        "Überschreitungen Kategorien pro Tag": daily_exceedance_categories,
        "Beschleunigt/Gebremst": acceleration_braking_stats
    }