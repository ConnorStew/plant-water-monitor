# Plant Water Monitor

I had an old raspberry pi lying around so I decided to turn it into a water monitor for my plants.

This code is deployed onto a raspberry pi 1 so it's too old for GitHub Actions runners, I've left the deployment as rsyncing to the pi instead.

Currently the project does the following:
  - Checks if the plant state changes to/from wet/dry and plays a dry/watered sound.
    - Only plays during active hours 9am-9pm
  - Plays a welcome sound on startup.
  - Lights up a connected LED based on water level.

## Sounds and Test CLI

I haven't included any generic sounds, so you'll need to add your own if you want to reproduce the build.

Add your sounds to the following folders before deploying:
  - water-monitor/audio/sounds/dry
  - water-monitor/audio/sounds/watered
  - water-monitor/audio/sounds/welcome

There's also a small cli for testing sounds `play_sound.py`, which can:
  - Play a specified file: `--file`
  - Play a sound from the three categories: `uv run play_sound.py` with: `dry`, `watered`, `welcome`
  - List sounds loaded: `--list`

## Development
- Create the venv: `uv sync`

## Deployment & Testing

Push:
```bash
rsync -avz --exclude-from='./deployment/.rsyncignore' ./ <user>@<pi-ip>:~/water-monitor
sudo systemctl restart water-monitor.service
```

Test:
```bash
ssh <user>@<pi-ip>
uv run ~/water-monitor/water-monitor/main.py
```

Init Service:
```bash
scp ./deployment/water-monitor.service <user>@<pi-ip>:~/water-monitor
sudo mv ~/water-monitor/water-monitor.service /etc/systemd/system
sudo systemctl enable --enable-now water-monitor.service
sudo systemctl status water-monitor.service
sudo journalctl -u water-monitor.service
```

## Setup

Using a Raspberry Pi 1. See `images/board.png` for the pin layout.

### Wiring

**Water Sensor**
| Wire | GPIO (BCM) | Physical Pin |
|------|-----------|--------------|
| Red (VCC) | 3.3V | Pin 1 |
| Black (GND) | GND | Pin 9 |
| Green (Signal) | GPIO18 | Pin 12 |

**LEDs** (each with a resistor to GND)
| Colour | GPIO (BCM) | Physical Pin |
|--------|-----------|--------------|
| Green | GPIO17 | Pin 11 |
| Red | GPIO23 | Pin 16 |
| Blue | GPIO22 | Pin 15 |
| GND (breadboard) | GND | Pin 6 |

## Docs

The water sensor is a CQRobot Contact Multi-Point Photoelectric Liquid Level Sensor (SKU: CQRSENYW003). The original documentation site is no longer online; `images/water_outputs.png` preserves the output frequency table and sensor diagram from it.