# Make this script running from every dir
import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.absolute())

import logging
from logconfig import configure_logging
from pathlib import Path
from common import Config
from camera import PiCamera
from display import Display
from app import Application
from gpiozero import Button
from signal import pause

if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Configured logging.")

    config = Config(image_dir=Path("/home/felix/data"))
    logger.info("Created configuration.")
    camera = PiCamera()
    logger.info("Created campera.")
    display = Display(gpio_DC=24, gpio_RST=25)
    logger.info("Created display.")
    app   = Application(config, camera, display)
    logger.info("Created application.")

    key1  = Button(pin=21)
    key2  = Button(pin=20)
    key3  = Button(pin=16)
    up    = Button(pin=6)
    down  = Button(pin=19)
    left  = Button(pin=5)
    right = Button(pin=26)
    press = Button(pin=13)
    logger.info("Created controls.")

    # Set event handlers for the buttons
    key1.when_pressed = app.capture_image
    key3.when_pressed = display.clear
    logger.info("Started application.")

    pause()
    logger.info("Exiting main thread.")
