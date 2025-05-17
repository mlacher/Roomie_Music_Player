import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
import time

# Funktion zum Einlesen der Konfiguration aus der config.json
def load_config():
    with open("config.json") as config_file:
        return json.load(config_file)

# Konfiguration laden
config = load_config()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["client_id"],
    client_secret=config["client_secret"],
    redirect_uri=config["redirect_uri"],  # URI aus der Konfiguration
    scope=config["scope"]  # Scope aus der Konfiguration
))

# Funktion zur Überprüfung und Ausgabe der aktiven Geräte
def check_devices():
    while True:
        # Hole aktuelle Zeit im Format h:m:s
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"Überprüfung gestartet um: {timestamp}")
        
        # Holen der Gerätedaten von Spotify
        devices = sp.devices()
        
        # Überprüfen, ob Geräte existieren
        if not devices['devices']:
            print("Keine Geräte gefunden.")
        
        for d in devices['devices']:
            # Ausgabe des Gerät Namens und der ID
            print(f"{d['name']} — {d['id']}")
            if d['is_active']:
                print(f"✅ {d['name']} ist aktiv.")
            else:
                print(f"❌ {d['name']} ist inaktiv.")
        
        print("-" * 50)  # Trennlinie für Übersichtlichkeit
        
        # Warten für 10 Sekunden, bevor wir die Geräte erneut überprüfen
        time.sleep(10)

# Starte die Überprüfung der Geräte
check_devices()
