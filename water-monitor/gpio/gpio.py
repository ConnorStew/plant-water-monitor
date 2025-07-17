import time
import signal
import logging
import sys
import RPi.GPIO as rpi_gpio

from water_monitor.water_level import WaterLevel
from gpio.pins import Pins

class GPIO:
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

    def show_level(self, level: WaterLevel) -> None:
        logging.info(f"Detected Level: {level.name}")

        for pin in Pins.values():
            rpi_gpio.output(pin, rpi_gpio.LOW)

        if level == WaterLevel.WITHOUT_LIQUID:
            rpi_gpio.output(Pins.GREEN_LED, rpi_gpio.HIGH)
        elif level in (WaterLevel.DP_1_WITH_LIQUID, WaterLevel.DP_2_WITH_LIQUID):
            rpi_gpio.output(Pins.RED_LED, rpi_gpio.HIGH)
        elif level in (WaterLevel.DP_3_WITH_LIQUID, WaterLevel.DP_4_WITH_LIQUID):
            rpi_gpio.output(Pins.BLUE_LED, rpi_gpio.HIGH)

    def cleanup(self, signum=None, frame=None):
        print("Cleaning up resources...")
        rpi_gpio.cleanup()
        sys.exit(0)