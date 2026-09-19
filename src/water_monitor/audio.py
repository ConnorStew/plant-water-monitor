from pathlib import Path
import simpleaudio as sa
from pydub import AudioSegment
import random
from datetime import datetime

from water_monitor.logger import logger

# res/ lives at the repo root, outside the package: src/water_monitor/audio.py
SOUNDS_FOLDER = Path(__file__).resolve().parents[2] / "res" / "sounds"

class Audio:
    DRY_SOUNDS_FOLDER = SOUNDS_FOLDER / "dry"
    WATERED_SOUNDS_FOLDER = SOUNDS_FOLDER / "watered"
    WELCOME_SOUNDS_FOLDER = SOUNDS_FOLDER / "welcome"

    BOOST_LEVELS = {
        "dry": {},
        "watered": {},
        "welcome": {
            "ninja-hello.wav": 25.0,
        },
    }

    def __init__(self):
        logger.info("Preloading sounds... 🔉")
        self._pending: dict[str, list[sa.WaveObject]] = {}
        self._in_quiet_hours: bool = not self._is_allowed_hour()

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
            f"{len(self.welcome_sounds)} welcome sounds."
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
        self._play_random(self.welcome_sounds, "welcome", skip_quiet_hours=True)

    def tick(self) -> None:
        """Call each loop iteration to flush queued sounds when quiet hours end."""
        now_quiet = not self._is_allowed_hour()
        if self._in_quiet_hours and not now_quiet and self._pending:
            logger.info("Quiet hours ended, playing queued sounds.")
            for label, sound_list in self._pending.items():
                self._play_sound(sound_list, label)
            self._pending.clear()
        self._in_quiet_hours = now_quiet

    def _is_allowed_hour(self) -> bool:
        return 9 <= datetime.now().hour < 21

    def _play_random(self, sound_list: list[sa.WaveObject], label: str, skip_quiet_hours: bool = False) -> None:
        if not sound_list:
            logger.warning(f"No sounds loaded in the '{label}' category.")
            return

        if not skip_quiet_hours and not self._is_allowed_hour():
            logger.debug(f"Queuing '{label}' sound until quiet hours end.")
            self._pending[label] = sound_list
            return

        self._play_sound(sound_list, label)

    def _play_sound(self, sound_list: list[sa.WaveObject], label: str) -> None:
        sound = random.choice(sound_list)
        sound.play()