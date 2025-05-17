import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import logging

def init_pn532(max_retries=3, delay=2):
    retries = 0
    while retries < max_retries:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            pn532 = PN532_I2C(i2c, debug=False)

            # Firmware-Version ausgeben
            ic, ver, rev, support = pn532.firmware_version
            print(f"Found PN532 with firmware version: {ver}.{rev}")

            # NFC konfigurieren
            pn532.SAM_configuration()
            return pn532

        except Exception as e:
            retries += 1
            logging.error(f"Fehler beim Initialisieren des PN532 (Versuch {retries} von {max_retries}): {e}")
            print(f"Fehler beim Initialisieren des PN532. Versuch {retries} von {max_retries} fehlgeschlagen.")
            time.sleep(delay)

    print("Fehler beim Initialisieren des PN532. Siehe error.log für Details.")
    return None



def read_nfc_with_retry(pn532,max_retries=3, delay=2):
    retries = 0
   
    while retries < max_retries:
        try:
            return pn532.read_passive_target(timeout=0.5)
        except Exception as e:
            retries += 1  # Erhöht den retry Zähler
            logging.warning(f"Fehler beim Lesen des PN532 (Versuch {retries}/{max_retries}): {e}")
            time.sleep(delay)
            if retries >= max_retries:
                logging.error("PN532 wird neu initialisiert...")
                pn532 = init_pn532()
    return None