import sys
from data_loader import lade_daten
from analyse_funktional import (
    schnellste_langsamste_pro_monat,
    anzahl_ueberschreitungen_pro_monat,
    durchschnittsgeschwindigkeit_pro_stunde,
    ueberschreitungen_nach_bereich,
    beschleunigung_verzoegerung
)
from analyse_imperativ import (
    schnellste_langsamste_pro_monat_imperativ,
    anzahl_ueberschreitungen_pro_monat_imperativ,
    durchschnittsgeschwindigkeit_pro_stunde_imperativ,
    ueberschreitungen_nach_bereich_imperativ,
    beschleunigung_verzoegerung_imperativ
)
from utils import drucke_ergebnis

def hauptfunktion(command):
    daten = lade_daten('../data/messungen.json')
    
    if command == "funktional schnellste_langsamste":
        result = schnellste_langsamste_pro_monat(daten)
        drucke_ergebnis("Höchste und Tiefste Einfahrtgeschwindigkeit pro Monat (Funktional)", result)
        
    elif command == "imperativ schnellste_langsamste":
        result = schnellste_langsamste_pro_monat_imperativ(daten)
        drucke_ergebnis("Höchste und Tiefste Einfahrtgeschwindigkeit pro Monat (Imperativ)", result)

    elif command == "funktional ueberschreitungen":
        result = anzahl_ueberschreitungen_pro_monat(daten)
        drucke_ergebnis("Anzahl der Überschreitungen pro Monat (Funktional)", result)

    elif command == "imperativ ueberschreitungen":
        result = anzahl_ueberschreitungen_pro_monat_imperativ(daten)
        drucke_ergebnis("Anzahl der Überschreitungen pro Monat (Imperativ)", result)
    
    elif command == "funktional durchschnittsgeschwindigkeit":
        result = durchschnittsgeschwindigkeit_pro_stunde(daten)
        drucke_ergebnis("Durchschnittsgeschwindigkeit pro Stunde (Funktional)", result)

    elif command == "imperativ durchschnittsgeschwindigkeit":
        result = durchschnittsgeschwindigkeit_pro_stunde_imperativ(daten)
        drucke_ergebnis("Durchschnittsgeschwindigkeit pro Stunde (Imperativ)", result)

    elif command == "funktional ueberschreitungen_bereich":
        result = ueberschreitungen_nach_bereich(daten)
        drucke_ergebnis("Überschreitungen nach Bereich (Funktional)", result)

    elif command == "imperativ ueberschreitungen_bereich":
        result = ueberschreitungen_nach_bereich_imperativ(daten)
        drucke_ergebnis("Überschreitungen nach Bereich (Imperativ)", result)

    elif command == "funktional beschleunigung_verzoegerung":
        result = beschleunigung_verzoegerung(daten)
        drucke_ergebnis("Beschleunigung/Verzögerung (Funktional)", result)

    elif command == "imperativ beschleunigung_verzoegerung":
        result = beschleunigung_verzoegerung_imperativ(daten)
        drucke_ergebnis("Beschleunigung/Verzögerung (Imperativ)", result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Bitte einen Befehl angeben!")
    else:
        command = sys.argv[1]
        hauptfunktion(command)
