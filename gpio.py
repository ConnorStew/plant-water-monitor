import RPi.GPIO as GPIO
import time

# Pin setup
GREEN_LED_PIN = 17
RED_LED_PIN = 23
BLUE_LED_PIN = 22
SENSOR_PIN = 18

led_pins = (GREEN_LED_PIN, RED_LED_PIN, BLUE_LED_PIN)

# Frequency thresholds for each level
FREQ_LEVELS = {
    "Without Liquid": (0, 40), # 20Hz
    "DP 1 With Liquid": (41, 80), # 50Hz
    "DP 2 With Liquid": (81, 150), # 100 Hz
    "DP 3 With Liquid": (151, 280), # 200 Hz
    "DP 4 With Liquid": (281, 1000) # 400Hz
}

SAMPLE_DURATION = 1.0  # seconds

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SENSOR_PIN, GPIO.IN)
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)

def cleanup():
    GPIO.cleanup()

def measure_frequency(pin, duration=1.0):
    """Count rising edges over the given time to estimate frequency."""
    count = 0
    start = time.time()
    end = start + duration
    last = GPIO.input(pin)

    while time.time() < end:
        current = GPIO.input(pin)
        if current == GPIO.HIGH and last == GPIO.LOW:
            count += 1
        last = current
    return count / duration

def show_level(level):
    print(f"Detected Level: {level}")
    # Reset all LEDs
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)

    if level == "Low":
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    elif level == "Medium":
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
        GPIO.output(RED_LED_PIN, GPIO.HIGH)
    elif level == "High":
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)

def map_frequency_to_level(freq):
    for level, (low, high) in FREQ_LEVELS.items():
        if low <= freq <= high:
            return level
    return "Unknown"

def main():
    setup()
    try:
        while True:
            freq = measure_frequency(SENSOR_PIN, SAMPLE_DURATION)
            print(f"Measured Frequency: {freq:.1f} Hz")

            level = map_frequency_to_level(freq)
            show_level(level)

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting gracefully")
        cleanup()

main()
