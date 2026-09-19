import time

from gpio.gpio import GPIO
from water_monitor.water_monitor import WaterMonitor
from water_monitor.water_level import WaterLevel
from audio.audio import Audio
from logger import logger

def main() -> None:
    logger.debug("💧 Starting monitoring... 🪴")

    gpio = GPIO()
    water_monitor = WaterMonitor()
    audio = Audio()

    audio.play_random_welcome()

    previous_level = None

    while True:
        freq = gpio.measure_frequency()
        logger.debug(f"Measured Frequency: {freq:.1f} Hz")

        level = water_monitor.map_frequency_to_level(freq)
        logger.info(f"Matched level: {level}")

        gpio.show_level(level)

        if level != previous_level:
            if level == WaterLevel.WITHOUT_LIQUID:
                audio.play_random_dry()
            elif level != WaterLevel.UNKNOWN:
                audio.play_random_watered()
            previous_level = level

        audio.tick()

        time.sleep(0.2)

if __name__ == "__main__":
    main()