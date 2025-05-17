import board
import busio
import adafruit_pn532.i2c
import time

# I2C initialisieren
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = adafruit_pn532.i2c.PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()

tag_present = False
uid = None

while True:
    if not tag_present:
        uid_try = pn532.read_passive_target(timeout=0.5)
        if uid_try:
            uid = uid_try
            print(f"Tag erkannt! UID: {uid.hex()}")
            tag_present = True
            time.sleep(0.5)  # kleine Pause vor dem ersten Zugriff
    else:
        try:
            # Versuch, Daten zu lesen
            data = pn532.ntag2xx_read_block(4)
            if data is None:
                raise RuntimeError("Keine Daten erhalten")
            print("Tag noch vorhanden – Block gelesen.")
        except Exception as e:
            print(f"Tag entfernt oder Lesefehler: {e}")
            tag_present = False
            uid = None
        time.sleep(0.3)
