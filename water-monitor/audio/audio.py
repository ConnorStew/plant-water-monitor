from pathlib import Path
import simpleaudio as sa
from pydub import AudioSegment
import random

from logger import logger

class Audio:
    DRY_SOUNDS_FOLDER = Path(__file__).parent / "sounds" / "dry"
    WATERED_SOUNDS_FOLDER = Path(__file__).parent / "sounds" / "watered"
    WELCOME_SOUNDS_FOLDER = Path(__file__).parent / "sounds" / "welcome"

    BOOST_LEVELS = {
        "dry": {},
        "watered": {},
        "welcome": {
            "ninja-hello.wav": 25.0,
        },
    }

    def __init__(self):
        logger.info("Preloading sounds... 🔉")

        self.dry_sounds = self._load_sounds_from_folder(
            self.DRY_SOUNDS_FOLDER, self.BOOST_LEVELS.get("dry", {})
        )
        self.watered_sounds = self._load_sounds_from_folder(
            self.WATERED_SOUNDS_FOLDER, self.BOOST_LEVELS.get("watered", {})
        )
        self.welcome_sounds = self._load_sounds_from_folder(
            self.WELCOME_SOUNDS_FOLDER, self.BOOST_LEVELS.get("welcome", {})
        )

        logger.info(
            f"Preloaded {len(self.dry_sounds)} dry, "
            f"{len(self.watered_sounds)} watered, and "
            f"{len(self.welcome_sounds)} welcome sounds ✅"
        )

    def _load_sounds_from_folder(self, folder: Path, boost_map: dict[str, float]) -> list[sa.WaveObject]:
        sounds = []
        for file in folder.glob("*.wav"):
            try:
                if file.name in boost_map:
                    gain_dB = boost_map[file.name]
                    sounds.append(self._load_and_amplify(file, gain_dB))
                    logger.info(f"Boosted {file.name} by {gain_dB} dB")
                else:
                    sounds.append(sa.WaveObject.from_wave_file(str(file)))
            except Exception as e:
                logger.warning(f"Failed to load {file.name}: {e}")
        return sounds

    def _load_and_amplify(self, file_path: Path, gain_dB: float) -> sa.WaveObject:
        seg = AudioSegment.from_wav(file_path)
        louder = seg + gain_dB
        return sa.WaveObject(
            louder.raw_data,
            num_channels=louder.channels,
            bytes_per_sample=louder.sample_width,
            sample_rate=louder.frame_rate
        )
    
    def play_random_dry(self) -> None:
        self._play_random(self.dry_sounds, "dry")

    def play_random_watered(self) -> None:
        self._play_random(self.watered_sounds, "watered")

    def play_random_welcome(self) -> None:
        self._play_random(self.welcome_sounds, "welcome")

    def _play_random(self, sound_list: list[sa.WaveObject], label: str) -> None:
        if not sound_list:
            logger.warning(f"No sounds loaded in the '{label}' category.")
            return

        sound = random.choice(sound_list)
        sound.play()