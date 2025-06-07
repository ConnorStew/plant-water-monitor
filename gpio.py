import RPi.GPIO as GPIO
import time

GREEN_LED_PIN = 17
RED_LED_PIN = 23
BLUE_LED_PIN = 22
SLEEP_TIME = 0.5

pins = (GREEN_LED_PIN, RED_LED_PIN, BLUE_LED_PIN)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

def cleanup():
    GPIO.cleanup()

# --- LED Patterns ---

def pattern_all_on_then_off():
    print("Pattern: All ON then OFF")
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(SLEEP_TIME)
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
    time.sleep(SLEEP_TIME)

def pattern_blink_one_by_one():
    print("Pattern: Blink One by One")
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(SLEEP_TIME)
        GPIO.output(pin, GPIO.LOW)


def main():
    setup()
    print(f"Running on pins: {pins}")

    patterns = [
        pattern_blink_one_by_one,
    ]

    try:
        while True:
            for pattern in patterns:
                pattern()
    except KeyboardInterrupt:
        print("Exiting gracefully")
        cleanup()

main()
