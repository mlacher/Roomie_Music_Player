import pychromecast
import zeroconf
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from config import load_config



config = load_config()
# Spotify Authentifizierung (ersetze mit deinen eigenen Anmeldedaten)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["client_id"],
    client_secret=config["client_secret"],
    redirect_uri=config["redirect_uri"],
    scope=config["scope"]
))


# Erstelle eine Zeroconf-Instanz
zeroconf_instance = zeroconf.Zeroconf()

# Alle verfügbaren Geräte im Netzwerk suchen
chromecasts, browser = pychromecast.get_chromecasts(zeroconf_instance=zeroconf_instance)




# Jetzt kannst du das gewünschte Gerät auswählen
cast = next(cc for cc in chromecasts if cc.name == "NestHub20B9")
print(f"✅ Verbunden mit: {cast.name}")

cast.wait()
# Zugriff auf den Chromecast-Controller
media_controller = cast.media_controller

# Die Geräte-ID abrufen (wir nutzen jetzt `cast.device.id`)

# Jetzt können wir das Spotify-Device steuern
print(f"Spotify auf {cast.name} bereit zum Steuern.")


