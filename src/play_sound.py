#!/usr/bin/env python3
"""
Usage:
  uv run play_sound.py [dry|watered|welcome]        # play random from category
  uv run play_sound.py --file <filename.wav>        # play specific sound by name
  uv run play_sound.py --list                       # list all available sounds
"""
import sys
import time
import simpleaudio as sa

from audio.audio import Audio

CATEGORIES = ("dry", "watered", "welcome")

FOLDERS = {
    "dry": Audio.DRY_SOUNDS_FOLDER,
    "watered": Audio.WATERED_SOUNDS_FOLDER,
    "welcome": Audio.WELCOME_SOUNDS_FOLDER,
}

def find_sound(filename: str):
    for category, folder in FOLDERS.items():
        path = folder / filename
        if path.exists():
            return path, category
    return None, None

def list_sounds():
    for category, folder in FOLDERS.items():
        sounds = sorted(folder.glob("*.wav"))
        print(f"\n{category}:")
        for s in sounds:
            print(f"  {s.name}")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

arg = sys.argv[1]

if arg == "--list":
    list_sounds()
    sys.exit(0)

if arg == "--file":
    if len(sys.argv) < 3:
        print("Usage: uv run play_sound.py --file <filename.wav>")
        sys.exit(1)
    path, category = find_sound(sys.argv[2])
    if path is None:
        print(f"Sound '{sys.argv[2]}' not found in any category.")
        sys.exit(1)
    print(f"Playing {path.name} ({category})")
    sa.WaveObject.from_wave_file(str(path)).play()
    time.sleep(5)
    sys.exit(0)

if arg not in CATEGORIES:
    print(f"Usage: uv run play_sound.py [{' | '.join(CATEGORIES)}]")
    print(f"       uv run play_sound.py --file <filename.wav>")
    print(f"       uv run play_sound.py --list")
    sys.exit(1)

audio = Audio()

if arg == "dry":
    audio.play_random_dry()
elif arg == "watered":
    audio.play_random_watered()
elif arg == "welcome":
    audio.play_random_welcome()

time.sleep(5)
