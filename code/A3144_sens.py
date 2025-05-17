
import logging
import RPi.GPIO as GPIO
import time

# GPIO Pins für die Hall-Sensoren
SENSOR_1_PIN = 23
SENSOR_2_PIN = 24
TIME_WINDOW = 1.5  # Zeitfenster in Sekunden
TIME_WINDOW_TRIGGER = 1.5 # Zeitfenster für Trigger in Sekunden

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_1_PIN, GPIO.IN)
GPIO.setup(SENSOR_2_PIN, GPIO.IN)

last_trigger_1 = None
last_trigger_2 = None

def check_direction():
    global last_trigger_1, last_trigger_2
    current_time = time.time()

    sensor_1_state = GPIO.input(SENSOR_1_PIN)
    sensor_2_state = GPIO.input(SENSOR_2_PIN)

    print(f"S1: {sensor_1_state} | S2: {sensor_2_state}")
    # CW Pattern: Sensor 1 → Sensor 2
    if sensor_1_state == GPIO.LOW and last_trigger_1 is None:
        last_trigger_1 = current_time
        print(f"Trigger 1 gesetzt: {last_trigger_1}")
        print(current_time - last_trigger_1)

    elif sensor_2_state == GPIO.LOW and last_trigger_1:
        # Prüfe, ob Sensor 2 innerhalb des Zeitfensters nach Sensor 1 LOW geht
        print(current_time - last_trigger_1)
        if current_time - last_trigger_1 <= TIME_WINDOW_TRIGGER:
            print("Drehrichtung: CW")
            # Nach einer erfolgreichen Erkennung sofort resetten
            last_trigger_1 = None
            last_trigger_2 = None
            return "CW"
        else:
            last_trigger_1 = None
            last_trigger_2 = None

    # CCW Pattern: Sensor 2 → Sensor 1


    if sensor_2_state == GPIO.LOW and last_trigger_2 is None:
        last_trigger_2 = current_time
        print(f"Trigger 2 gesetzt: {last_trigger_2}")
        print(current_time - last_trigger_2)


    elif sensor_1_state == GPIO.LOW and last_trigger_2:
        # Prüfe, ob Sensor 1 innerhalb des Zeitfensters nach Sensor 2 LOW geht
        print(current_time - last_trigger_2)

        if current_time - last_trigger_2 <= TIME_WINDOW_TRIGGER:
            print("Drehrichtung: CCW")
            last_trigger_1 = None
            last_trigger_2 = None
            return "CCW"
        else:
            last_trigger_1 = None
            last_trigger_2 = None

    # Reset both triggers if both sensors are HIGH and within the time window
    if (sensor_1_state == GPIO.HIGH and sensor_2_state == GPIO.HIGH and 
        ((last_trigger_1 and current_time - last_trigger_1 >= TIME_WINDOW) or 
         (last_trigger_2 and current_time - last_trigger_2 >= TIME_WINDOW))): 
        last_trigger_1 = None
        last_trigger_2 = None

    return None


def main_loop():
    try:
        while True:
            check_direction()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Beende Programm")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main_loop()