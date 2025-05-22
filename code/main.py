import time
from mariaDB import init_db, devices_db, songs_db, history_db
from pn532_init import init_pn532, read_nfc_with_retry
from config import load_config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_control import init_spotify, find_song_by_nfc, music_control
from A3144_sens import check_direction
import logging
import RPi.GPIO as GPIO

# Basic Logging Setup
logging.basicConfig(
    filename='error.txt',  # Log-Datei
    level=logging.INFO,  # Informationslevel
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

def main():
    config = load_config()
    print(config["database"])
    db_connection = init_db(config["database"])
    devices = devices_db(db_connection)
    songs = songs_db(db_connection)
    if not db_connection:
        logging.error("Fehler beim Verbinden mit der Datenbank. Beende das Programm.")
        return

    pn532 = init_pn532()
    sp = init_spotify(config["spotify"], devices[4][0])
    last_uid = None
    last_nfc_check = time.time()
    last_direction_check = time.time()
    last_auto_check = time.time()


    try:
        while True:
            current_time = time.time()

            # Check direction alle 0.05 Sekunden
            if current_time - last_direction_check >= 0.05:
                direction = check_direction()
                if direction == "CCW":
                    music_control(sp, devices[4], None, "previous")
                elif direction == "CW":
                    music_control(sp, devices[4], None, "next")
                last_direction_check = current_time

            # NFC-Check alle 0.1 Sekunden
            if current_time - last_nfc_check >= 0.1:
                uid = read_nfc_with_retry(pn532)
                last_nfc_check = current_time

                if uid is not None:
                    uid_hex = ''.join([f'{x:02X}' for x in uid])
                    print(f"Richtung: {direction}")

                    if uid_hex != last_uid:
                        logging.info(f"Neue UID erkannt: {uid_hex}")
                        song_id = find_song_by_nfc(uid_hex, songs)
                        if song_id:
                            music_control(sp, devices[4], songs[song_id[0]], "new_UID")
                            history_db(db_connection, devices[4], songs[song_id[0]])
                        else:
                            logging.info(f"Keine Zuordnung für UID {uid_hex} gefunden.")

                        last_uid = uid_hex
                        time.sleep(2)
                    else:
                        logging.info("Gleiches Tag wie vorher – ignoriere.")
                        if time.time() - last_auto_check >= 5:
                            music_control(sp, devices[4], songs[song_id[0]], "auto")
                            last_auto_check = time.time()
                else:
                    if last_uid is not None:
                        music_control(sp, devices[4], None, "pause")
                        last_uid = None

    except KeyboardInterrupt:
        logging.info("Programm beendet.")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
