# Fauna-Eye

Fauna-Eye is a wildlife observation system for my backyard. It detects
movement, captures images, identifies animal species, and sends notifications.

[Context Diagram](docs/context.png)

## About

Once, in the mid of the night, I saw a fox staring trough our terrace toor for a
brief moment before it rushed off. When I told my wife the next day, we got very
curious which animals visit our garden (everyone is welcome, except snails and
mosquitoes). I then came up with the plan to build my own wildlife observation
system.

## Roadmap

### Stage 1

- [x] Setup Hardware
- [ ] Capture Image with the camera
- [ ] Trigger image from motion sensor
- [ ] Transmit image to server
- [ ] Persist images and metadata
- [ ] WebUI to show and manage images
- [ ] Send notifications

### Stage 2

- [ ] Identify species using WEB-API
- [ ] Identify species using local model
- [ ] Use specied information to filter notifications
- [ ] Show species information in WebUI

### Stage 3

- [ ] Add a microphone
- [ ] Record bird voices
- [ ] Recognize bird species (BirdNET)
- [ ] Extend notifications
- [ ] Build a proper hardware case

## Documentation

[Architecture](docs/architecture.md)

## License

[MIT License](LICENSE)
