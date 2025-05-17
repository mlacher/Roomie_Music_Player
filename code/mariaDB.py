import mysql.connector
from datetime import datetime
import pytz



def init_db(db_config):
    try:
        # Verbindung zur MariaDB herstellen
        db_connection = mysql.connector.connect(
            host=db_config["host"],  # Hostname der Datenbank (z.B. localhost oder IP-Adresse)
            user=db_config["user"],  # Dein MariaDB-Benutzername
            password=db_config["password"],  # Dein MariaDB-Passwort
            database=db_config["database"]  # Der Name deiner Datenbank
        )

        print("Datenbank erfolgreich verbunden.")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None

def devices_db(db_connection):
    try:
        cursor = db_connection.cursor()
        # SQL-Abfrage, um alle Daten aus der Spotify_Devices Tabelle zu holen
        query = "SELECT * FROM Spotify_Devices"
        # Ausführen der Abfrage
        cursor.execute(query)
        # Alle Ergebnisse der Abfrage holen
        devices = cursor.fetchall()
        cursor.close()
        print(f"Geräte gelesen")
        return devices
        
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None

def songs_db(db_connection):
    try:
        cursor = db_connection.cursor()
        # SQL-Abfrage, um alle Daten aus der Spotify_Devices Tabelle zu holen
        query = "SELECT * FROM Songs"
        # Ausführen der Abfrage
        cursor.execute(query)
        # Alle Ergebnisse der Abfrage holen
        devices = cursor.fetchall()
        cursor.close()
        print(f"Songs gelesen")
        return devices
        
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None

def history_db(db_connection, device_data, song_data):
    try:
        berlin = pytz.timezone("Europe/Berlin")
        timestamp = datetime.now(berlin).strftime("%Y-%m-%d %H:%M:%S")
        cursor = db_connection.cursor()
        print(f"History: {device_data[0]} - {song_data[1]}")
        cursor.execute("""
            INSERT INTO Roomie_History (NFC_ID, DEVICE_ID, recorded_at)
            VALUES (%s, %s, %s)
        """, (song_data[1], device_data[0], timestamp))
        db_connection.commit()
        print("✅ History entry added.")
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None