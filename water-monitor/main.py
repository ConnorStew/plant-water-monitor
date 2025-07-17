import time
import logging
import sys

from gpio.gpio import GPIO

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    gpio = GPIO()

    while True:
        freq = gpio.measure_frequency()
        logging.info(f"Measured Frequency: {freq:.1f} Hz")

        level = gpio.map_frequency_to_level(freq)
        gpio.show_level(level)

        time.sleep(0.2)  # shorter delay for quicker updates

if __name__ == "__main__":
    main()

