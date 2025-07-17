import time

from gpio.gpio import GPIO
from water_monitor.water_montior import WaterMonitor
from logger import logger

def main() -> None:
    logger.debug("💧 Starting 🪴")

    gpio = GPIO()
    water_monitor = WaterMonitor()

    while True:
        freq = gpio.measure_frequency()
        logger.debug(f"Measured Frequency: {freq:.1f} Hz")

        level = water_monitor.map_frequency_to_level(freq)
        logger.info(f"Matched level: {level}")

        gpio.show_level(level)

        time.sleep(0.2)  

if __name__ == "__main__":
    main()