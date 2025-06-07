import RPi.GPIO as GPIO
from enum import Enum
import time

# Pin setup
GREEN_LED_PIN = 17
RED_LED_PIN = 23
BLUE_LED_PIN = 22
SENSOR_PIN = 18

led_pins = (GREEN_LED_PIN, RED_LED_PIN, BLUE_LED_PIN)

# Frequency thresholds for each level
class FrequencyLevel(Enum):
    UNKNOWN = 0
    WITHOUT_LIQUID = 1
    DP_1_WITH_LIQUID = 2
    DP_2_WITH_LIQUID = 3
    DP_3_WITH_LIQUID = 4
    DP_4_WITH_LIQUID = 5

FREQ_LEVELS = {
    FrequencyLevel.UNKNOWN: (-1,-1),
    FrequencyLevel.WITHOUT_LIQUID: (0, 40), # 20Hz
    FrequencyLevel.DP_1_WITH_LIQUID: (41, 80), # 50Hz
    FrequencyLevel.DP_2_WITH_LIQUID: (81, 150), # 100 Hz
    FrequencyLevel.DP_3_WITH_LIQUID: (151, 280), # 200 Hz
    FrequencyLevel.DP_4_WITH_LIQUID: (281, 1000) # 400Hz
}

SAMPLE_DURATION = 1.0  # seconds

def setup() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SENSOR_PIN, GPIO.IN)
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)

def cleanup() -> None:
    GPIO.cleanup()

def measure_frequency(pin, duration=1.0) -> int:
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

def show_level(level: FrequencyLevel) -> None:
    print(f"Detected Level: {level}")

    # Reset all LEDs
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)

    # Turn on LED
    match level:
        case FrequencyLevel.WITHOUT_LIQUID:
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

        case FrequencyLevel.DP_1_WITH_LIQUID | FrequencyLevel.DP_2_WITH_LIQUID:
            GPIO.output(RED_LED_PIN, GPIO.HIGH)

        case FrequencyLevel.DP_3_WITH_LIQUID | FrequencyLevel.DP_4_WITH_LIQUID:
            print("Liquid: {level}")
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH)

def map_frequency_to_level(freq: int) -> FrequencyLevel:
    for level, (low, high) in FREQ_LEVELS.items():
        if low <= freq <= high:
            return level
    
    return FrequencyLevel.UNKNOWN

def main() -> None:
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
