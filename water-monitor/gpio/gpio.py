import time
import signal
import logging
import sys
import RPi.GPIO as rpi_gpio

from water_monitor.frequency_level import FrequencyLevel
from gpio.pins import Pins

class GPIO:
    FREQ_LEVELS = {
        FrequencyLevel.UNKNOWN: (-1, -1),
        FrequencyLevel.WITHOUT_LIQUID: (0, 40), # 20Hz
        FrequencyLevel.DP_1_WITH_LIQUID: (41, 80), # 50Hz
        FrequencyLevel.DP_2_WITH_LIQUID: (81, 150), # 100 Hz
        FrequencyLevel.DP_3_WITH_LIQUID: (151, 280), # 200 Hz
        FrequencyLevel.DP_4_WITH_LIQUID: (281, 1000) # 400Hz
    }

    SAMPLE_DURATION = 0.5  # seconds

    def __init__(self) -> None:
        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGINT, self.cleanup)

        rpi_gpio.setmode(rpi_gpio.BCM)
        rpi_gpio.setwarnings(False)
        rpi_gpio.setup(Pins.SENSOR, rpi_gpio.IN, pull_up_down=rpi_gpio.PUD_DOWN)

        for pin in Pins.values():
            rpi_gpio.setup(pin, rpi_gpio.OUT)

    def measure_frequency(self) -> float:
        """Efficient edge-counting to determine frequency."""
        count = 0
        start_time = time.monotonic()
        end_time = start_time + self.SAMPLE_DURATION
        last_state = rpi_gpio.input(Pins.SENSOR)

        while time.monotonic() < end_time:
            current_state = rpi_gpio.input(Pins.SENSOR)
            if current_state == rpi_gpio.HIGH and last_state == rpi_gpio.LOW:
                count += 1
            last_state = current_state

        return count / self.SAMPLE_DURATION

    def map_frequency_to_level(self, freq: float) -> FrequencyLevel:
        for level, (low, high) in self.FREQ_LEVELS.items():
            if low <= freq <= high:
                return level
        return FrequencyLevel.UNKNOWN

    def show_level(self, level: FrequencyLevel) -> None:
        logging.info(f"Detected Level: {level.name}")

        for pin in Pins.values():
            rpi_gpio.output(pin, rpi_gpio.LOW)

        if level == FrequencyLevel.WITHOUT_LIQUID:
            rpi_gpio.output(Pins.GREEN_LED, rpi_gpio.HIGH)
        elif level in (FrequencyLevel.DP_1_WITH_LIQUID, FrequencyLevel.DP_2_WITH_LIQUID):
            rpi_gpio.output(Pins.RED_LED, rpi_gpio.HIGH)
        elif level in (FrequencyLevel.DP_3_WITH_LIQUID, FrequencyLevel.DP_4_WITH_LIQUID):
            rpi_gpio.output(Pins.BLUE_LED, rpi_gpio.HIGH)

    def cleanup(self, signum=None, frame=None):
        print("Cleaning up resources...")
        rpi_gpio.cleanup()
        sys.exit(0)