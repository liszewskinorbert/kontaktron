#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import datetime

# Konfiguracja pinu GPIO
GPIO_PIN = 17  # Pin, do którego podłączony jest kontaktron
LOG_FILE = "/var/log/kontaktron_log.txt"

# Ustawienia GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def log_event(state):
    """Zapisuje zdarzenie do pliku tekstowego."""
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - Stanu: {'Otwarte' if state else 'Zamknięte'}\n")

def main():
    last_state = GPIO.input(GPIO_PIN)
    log_event(last_state)  # Zapisz początkowy stan

    try:
        while True:
            current_state = GPIO.input(GPIO_PIN)
            if current_state != last_state:  # Stan zmienił się
                log_event(current_state)
                last_state = current_state
            time.sleep(0.1)  # Opóźnienie, aby zredukować wykorzystanie CPU
    except KeyboardInterrupt:
        print("Program został przerwany.")
    finally:
        GPIO.cleanup()  # Przywrócenie stanu GPIO

if __name__ == "__main__":
    main()

