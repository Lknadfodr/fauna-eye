# Architecture

This page documents the (planned) architecture of the system, both hardware
and software.

## Hardware

The system will be running distributed on two devices, an outdoor camera and my
homeserver. I first indended to use only one device, a Raspberry Pi 5, but due
to the current prices, I decided to use the hardware I already have. Eventually
the software modules will be containerized anyways, so deploying them on different
hardware later is no issue.

### Outdoor Sensor

- Raspberry Pi Zero 2 W
- Raspberry Camera Module 3 NoIR
- [PIR Motion Sensor HC-SR501](https://joy-it.net/files/files/Produkte/SEN-HC-SR501/SEN-HC-SR501_Manual_2024-04-16.pdf)
- [Waveshare 1.3" OLED HAT](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)

I chose the NoIR camera for nighttime pictures.
The OLED display is just for debugging and easier development.

![Wiring diagram](.assets/wiring.png)

I do not yet have a plan for a proper case, so I'll use a cardboard box for now.

### Homeserver

- UGREEN NASync DXP4800 (Intel N100, 8 GB RAM)

I plan to upgrade the RAM to 32 GB sometime in the future.

## Software

![Component Diagram](.assets/component.png)

### Outdoor Sensor

- Raspberry PI OS

I'll write a python script, maybe containerized, using standard modules for the
GPIO reading / camera / SPI protocol.

### Homeserver

- TrueNAS Scale

I plan to have one Docker container for each component, i.e. one for the
MQTT Broker, one for the WebUI, one for the database, etc. I didn't decide yet which
languages and frameworks to use.
