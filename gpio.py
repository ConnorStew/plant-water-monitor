import RPi.GPIO as GPIO
import time

PIN = 17
SLEEP_TIME = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN, GPIO.OUT)

try:
    while True:
        time.sleep(SLEEP_TIME)
        print("LED on")
        GPIO.output(PIN, GPIO.HIGH)

        time.sleep(SLEEP_TIME)
        print("LED off")
        GPIO.output(PIN, GPIO.LOW)
except KeyboardInterrupt:
    print("Exiting gracefully")
    GPIO.cleanup()