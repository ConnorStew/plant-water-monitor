import RPi.GPIO as GPIO
import time

GREEN_LED_PIN = 17
RED_LED_PIN = 23
BLUE_LED_PIN = 22
SLEEP_TIME = 1

def main():
    pins = (GREEN_LED_PIN, RED_LED_PIN, BLUE_LED_PIN)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    print(f"Running on pins: {pins}")

    try:
        while True:
            time.sleep(SLEEP_TIME)
            for pin in pins:
                print(f"Pin: {pin} on.")
                GPIO.output(pin, GPIO.HIGH)

            print(f"Sleeping: {SLEEP_TIME}")
            time.sleep(SLEEP_TIME)
            for pin in pins:
                print(f"Pin: {pin} off.")
                GPIO.output(pin, GPIO.LOW)
            print(f"Sleeping: {SLEEP_TIME}")
    except KeyboardInterrupt:
        print("Exiting gracefully")
        GPIO.cleanup()

main()