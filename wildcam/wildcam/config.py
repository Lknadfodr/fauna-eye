import os, dotenv
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """
    Stores config parameters.
    
    Attributes
    ----------
    upload_address : str
        HTTP address of the upload service.
    image_dir : Path
        Directory where images can be stored temporarily.
    gpio_key1 : int
        GPIO pin for key 1.
    gpio_key2 : int
        GPIO pin for key 2.
    gpio_key3 : int
        GPIO pin for key 3.
    gpio_up : int
        GPIO pin for the joystick 'up' (+y).
    gpio_down : int
        GPIO pin for the joystick 'down' (-y).
    gpio_left : int
        GPIO pin for the joystick 'left' (-x).
    gpio_right : int
        GPIO pin for the joystick 'right' (+x).
    gpio_press : int
        GPIO pin for the joystick 'press' (z).
    """
    upload_address: str
    image_dir: Path
    gpio_key1: int
    gpio_key2: int
    gpio_key3: int
    gpio_up: int
    gpio_down: int
    gpio_left: int
    gpio_right: int
    gpio_press: int

    def load():
        """ Loads the Config from .env and os.environ"""
        dotenv.load_dotenv()
        return Config(
            upload_address  =     os.getenv("UPLOAD_ADDRESS"),
            image_dir       =Path(os.getenv("IMAGE_DIR",  "data/")),
            gpio_key1       = int(os.getenv("GPIO_KEY1",  "21")),
            gpio_key2       = int(os.getenv("GPIO_KEY2",  "20")),
            gpio_key3       = int(os.getenv("GPIO_KEY3",  "16")),
            gpio_up         = int(os.getenv("GPIO_UP",    "6")),
            gpio_down       = int(os.getenv("GPIO_DOWN",  "19")),
            gpio_left       = int(os.getenv("GPIO_LEFT",  "5")),
            gpio_right      = int(os.getenv("GPIO_RIGHT", "26")),
            gpio_press      = int(os.getenv("GPIO_PRESS", "13"))
        )