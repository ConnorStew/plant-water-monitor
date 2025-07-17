from pathlib import Path
import simpleaudio as sa

from logger import logger

class Audio:
    DRY_SOUNDS_FOLDER = Path(__file__).parent / "sounds" / "dry"
    WATERED_SOUNDS_FOLDER = Path(__file__).parent / "sounds" / "watered"

    def __init__(self):
        logger.info("Preloading sounds... 🔉")
        self.watering_sound = sa.WaveObject.from_wave_file(str(self.WATERED_SOUNDS_FOLDER / "water-splash.wav"))
        logger.info("Preloading complete ✅ ")

    def play_sound(self) -> None:
        self.watering_sound.play()