# Raspberry-Pi-GPIO

## Commands

Push:
```bash
scp ./gpio.py ./requirements.txt connor@192.168.4.56:~/gpio
sudo systemctl restart water-monitor.service
```

Run:
```bash
ssh connor@192.168.4.56
cd gpio
source ./venv/bin/activate
python gpio.py
```

Init Service:
```bash
scp ./water-monitor.service connor@192.168.4.56:~/water-monitor
sudo mv /home/connor/water-monitor/water-monitor.service /etc/systemd/system
sudo systemctl enable --enable-now water-monitor.service
sudo systemctl status water-monitor.service
sudo journalctl -u water-monitor.service
```

## Setup

- Using a raspberry pi 1, the pins are in shown in the attached board image.

## Docs

- [Water Sensor Docs](http://www.cqrobot.wiki/index.php/Contact_Multi-point_Photoelectric_Liquid_Level_Sensor_SKU:_CQRSENYW003)