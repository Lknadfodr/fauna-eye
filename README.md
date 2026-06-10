# Fauna-Eye

Fauna-Eye is a wildlife observation system for my backyard. It detects
movement, captures images, identifies animal species, and sends notifications.

![Context Diagram](docs/.assets/context.png)

## About

Once, in the mid of the night, I saw a fox staring trough our terrace toor for a
brief moment before it rushed off. When I told my wife the next day, we got very
curious which animals visit our garden (everyone is welcome, except snails and
mosquitoes). I then came up with the plan to build my own wildlife observation
system.

> [!NOTE]
> This is a hobby project built primarily for learning and experimentation. I'm
> not optimizing for simplicity, but for experience and my personal satisfaction
> with the implementation. As a result, some parts are itentionally more complex
> than necessary. I still try to keep the code maintainable.

## Roadmap

### Stage 1

- [x] Setup Hardware
- [x] Capture Image with the camera
- [ ] Trigger image from motion sensor
- [x] Provide upload service
- [x] Transmit image to server
- [x] Queue uploads when not connected
- [ ] Persist images and metadata
- [ ] WebUI to show and manage images
- [ ] Send notifications

### Stage 2

- [ ] Identify species using WEB-API
- [ ] Identify species using local model
- [ ] Use species information to filter notifications
- [ ] Show species information in WebUI

### Stage 3

- [ ] Add a microphone
- [ ] Record bird voices
- [ ] Recognize bird species (BirdNET)
- [ ] Extend notifications
- [ ] Build a proper hardware case

## Repository structure

**develop**: Compose files to build and run components locally.
**docs**: Contains documentation.
**server**: Compose file, dotenv and configs of the server.
**upload-service**: A HTTP upload service with REST API.
**wildcam**: The application running on the outdoor camera.

## Get Started

1. Checkout this repository

### Build and run components locally

1. In *develop/* create a *.env* file and add your PUID and PGID.
2. `docker compose -f develop/compose.yml up`

This includes a wildcam service that generates artificial images.

### Run the wildcam on a Raspberry Pi

1. Enable [SPI](https://www.raspberrypi.com/documentation/computers/configuration.html#spi)
2. Checkout this repository or copy the wildcam onto the Pi
3. `sudo apt install python3-picamera2 python3-gpiozero python3-luma.oled python3-prompt-toolkit`
5. `cd wildcam && python -m wildcam`

## Documentation

[Architecture](docs/architecture.md)

## License

[MIT License](LICENSE)
