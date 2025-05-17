import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

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

devices = sp.devices()
for d in devices['devices']:
    print(f"{d['name']} — {d['id']}")

