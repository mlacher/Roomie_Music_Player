import time
import random
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import logging 

shuffle_list = []
current_index = -1
last_play_mode = None

import subprocess

def restart_raspotify():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'raspotify'], check=True)
        print("Raspotify neu gestartet")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Neustarten von Raspotify: {e}")





# Initialisierung von Spotify

def init_spotify(sp_config, device_name):
    attempt = 0
    sp = None
    while attempt < 3:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=sp_config["client_id"],
                client_secret=sp_config["client_secret"],
                redirect_uri=sp_config["redirect_uri"],
                scope=sp_config['scope']
            ))
            devices = sp.devices()['devices']
            for device in devices:
                if device['name'] == device_name:
                    print(f"Gerät {device_name} gefunden")
                    return sp
            print(f"Gerät {device_name} nicht gefunden. Versuche erneut...")
            restart_raspotify()
            time.sleep(5)
        except Exception as e:
            print(f"Fehler bei der Spotify-Initialisierung: {e}")
        attempt += 1

    logging.error("Gerät nicht gefunden. Initialisierung fehlgeschlagen.")
    return None

# Geräte abrufen

def get_available_devices(sp):
    devices = sp.devices()['devices']
    return devices

# Playlist-URIs abrufen

def get_track_uris_from_playlist(sp, playlist_id, shuffle=False):
    track_uris = []
    try:
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    track_uris.append(track['uri'])
            if results['next']:
                results = sp.next(results)
            else:
                break
    except Exception as e:
        logging.info(f"Fehler beim Laden der Playlist: {e}")
    if shuffle:
        random.shuffle(track_uris)
    return track_uris

# NFC-Song Suche

def find_song_by_nfc(nfc_id, song_list):
    for index, song in enumerate(song_list):
        if song[0] == nfc_id:
            return index, song
    return None, None

# Music Control Funktion

def music_control(sp, device_data, song_data, play_mode):
    global shuffle_list, current_index, last_play_mode
    device_id = device_data[1]
    playlist_flag = song_data[4] if song_data else 0

    try:
        if play_mode != last_play_mode:
            # Playlist-Modus aktivieren
            if play_mode == "new_UID" and song_data:
                track_id = song_data[3]
                if playlist_flag == 1:
                    # Playlist laden und shufflen
                    shuffle_list = get_track_uris_from_playlist(sp, track_id, shuffle=True)
                    if shuffle_list:
                        current_index = 0
                        sp.start_playback(device_id=device_id, uris=[shuffle_list[current_index]])
                        logging.info(f"Starte Shuffle-Track: {shuffle_list[current_index]}")
                else:
                    # Einzelner Song
                    track_uri = f"spotify:track:{track_id.strip()}"
                    shuffle_list = [track_uri]
                    current_index = 0
                    sp.start_playback(device_id=device_id, uris=[track_uri])
                    logging.info(f"Spiele Einzelsong: {track_uri}")

            elif play_mode == "pause":
                sp.pause_playback(device_id=device_id)
                logging.info("Wiedergabe pausiert.")

            elif play_mode == "play":
                sp.start_playback(device_id=device_id)
                logging.info("Wiedergabe gestartet.")

            elif play_mode == "next":
                if shuffle_list and current_index < len(shuffle_list) - 1:
                    current_index += 1
                    sp.start_playback(device_id=device_id, uris=[shuffle_list[current_index]])
                    logging.info(f"Nächster Shuffle-Track: {shuffle_list[current_index]}")
                else:
                    logging.info("Ende der Shuffle-Liste erreicht.")

            elif play_mode == "previous":
                if shuffle_list and current_index > 0:
                    current_index -= 1
                    sp.start_playback(device_id=device_id, uris=[shuffle_list[current_index]])
                    logging.info(f"Vorheriger Shuffle-Track: {shuffle_list[current_index]}")
                else:
                    logging.info("Am Anfang der Shuffle-Liste.")

        # Automatisches Weiterspielen unabhängig vom Playmode
        elif play_mode == "auto" and shuffle_list:
            current_track = sp.current_playback()
            if current_track and current_track.get("is_playing"):
                track_progress = current_track["progress_ms"]
                track_duration = current_track["item"]["duration_ms"]

                if track_progress >= track_duration - 1500:
                    if current_index < len(shuffle_list) - 1:
                        current_index += 1
                        sp.start_playback(device_id=device_id, uris=[shuffle_list[current_index]])
                        logging.info(f"Automatisch zum nächsten Shuffle-Track gewechselt: {shuffle_list[current_index]}")
                    else:
                        logging.info("Ende der Shuffle-Liste erreicht.")
            elif not current_track:
                logging.info("Keine Wiedergabe aktiv. Playlist wird fortgesetzt...")
                if shuffle_list and current_index < len(shuffle_list) - 1:
                    current_index += 1
                    sp.start_playback(device_id=device_id, uris=[shuffle_list[current_index]])
                    logging.info(f"Fortgesetzt mit: {shuffle_list[current_index]}")
                else:
                    logging.info("Playlist beendet.")

        # Aktualisierung des letzten Playmode-Status
        last_play_mode = play_mode

    except Exception as e:
        logging.error(f"Fehler in music_control: {e}")
