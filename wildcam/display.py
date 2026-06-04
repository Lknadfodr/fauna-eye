from luma.oled.device import sh1106
from luma.core.interface.serial import spi
from luma.core.render import canvas
from datetime import datetime

class Display:
    """ The display abstracts the SPI/IPC and the device driver protocols. 
        It provides high level-drawing methods.
    """
    def __init__(self, gpio_DC: int, gpio_RST: int):
        self.spi = spi(port=0, device=0, gpio_DC=gpio_DC, gpio_RST=gpio_RST)
        self.device = sh1106(self.spi)
        pass

    def show_message(self, time: datetime):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            text = f"Last: {time.isoformat()}"
            draw.text((4, 4), text, fill="white")
    
    def clear(self):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")