# Raspberry-Pi-GPIO

## Commands

Push:
```bash
scp ./gpio.py ./requirements.txt connor@192.168.4.56:~/gpio
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
scp ./gpio.service ./gpio_start.sh connor@192.168.4.56:~/gpio
sudo mv /home/connor/gpio/gpio.service /etc/systemd/system
sudo systemctl enable gpio.service
sudo systemctl status gpio.service
```

## Setup

- Using a raspberry pi 1, the pins are in shown in the attached board image.

## Docs

- [Water Sensor Docs](http://www.cqrobot.wiki/index.php/Contact_Multi-point_Photoelectric_Liquid_Level_Sensor_SKU:_CQRSENYW003)