# Raspberry-Pi-GPIO

## Commands

Push:
```bash
rsync -avz --exclude-from='./deployment/.rsyncignore' ./ connor@192.168.4.56:~/water-monitor
sudo systemctl restart water-monitor.service
```

Run:
```bash
ssh connor@192.168.4.56
uv run ~/water-monitor/water-monitor/main.py
```

Init Service:
```bash
scp ./deployment/water-monitor.service connor@192.168.4.56:~/water-monitor
sudo mv /home/connor/water-monitor/water-monitor.service /etc/systemd/system
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

- [Water Sensor Docs](http://www.cqrobot.wiki/index.php/Contact_Multi-point_Photoelectric_Liquid_Level_Sensor_SKU:_CQRSENYW003)