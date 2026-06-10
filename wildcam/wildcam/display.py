import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from http import HTTPStatus

class Display:
    """ 
    The display abstracts the SPI/IPC and device driver protocols. 
    It provides high level-drawing methods.
    """

    def render(self, ip: str, status: HTTPStatus, time: datetime | None, buffered: int):
        """ 
        Renders the given information. 
        
        Parameters
        ----------
        ip : str
            The local IP address.
        status : HTTPStatus
            Health status of the upload service 
        time : datetime
            Timestamp of the last picture.
        buffered : int
            Number of buffered images.
        """
        pass

    def clear(self):
        """ Clears the display. """
        pass

def create_display():
    """
    Creates a suitable display based on the environment. 
    
    On the Raspberry Pi, the SPI display is used. Otherwise the terminal is
    used as display.
    """
    try:
        import RPi # Only available on the Pi.
    except ImportError as e:
        logger.warning(e)
        logger.warning("SH1106 display will not be used.")
        return TerminalDisplay()
    return create_SH1106_display(gpio_DC=24, gpio_RST=25)


def create_SH1106_display(gpio_DC=24, gpio_RST=25):
    """ Creates a display that uses the SH1106 device driver. """

    # Lazy imports in case the package is not installed.
    from luma.oled.device import sh1106
    from luma.core.interface.serial import spi
    from luma.core.render import canvas

    bus = spi(port=0, device=0, gpio_DC=gpio_DC, gpio_RST=gpio_RST)
    device = sh1106(bus)

    class SH1106Display(Display):
        def render(self, ip: str, status: HTTPStatus, time: datetime | None, buffered: int):
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                text =  f"WLAN:  {ip}\n" +\
                        f"HTTP:  {status.name if status else "-"}\n" +\
                        f"Queue: {buffered:d}\n" +\
                        f"Last:  {time.isoformat(sep=" ", timespec="minutes") if time else ''}"
                draw.text((4, 4), text, fill="white")

        def clear(self): 
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="black", fill="black")

    return SH1106Display()

class TerminalDisplay(Display):
    """ This display renders onto the terminal using print statements. """

    def __init__(self):
        self._last = ""

    def render(self, ip: str, status: HTTPStatus, time: datetime | None, buffered: int):
        text =  f"  --------------------------------\n" +\
                f"  | WLAN:  {ip}\n" +\
                f"  | HTTP:  {status.name if status else "-"}\n" +\
                f"  | Queue: {buffered:d}\n" +\
                f"  | Last:  {time.isoformat(sep=" ", timespec="minutes") if time else ''}"
        if self._last != text:
            print(text)
            self._last = text
