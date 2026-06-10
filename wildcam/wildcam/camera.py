import logging
logger = logging.getLogger(__name__)

import asyncio
from datetime import datetime
from io import BytesIO
from wildcam.common import Picture

class Camera:
    """
    Interface for the camera. 
    
    The import statement for the picamera2 module raises in virtual 
    environments. One can use a system-site-packages venv and install
    python-libcamera, but I chose to hide the import behind an interface.
    """
    
    async def capture_picture(self) -> Picture:
        """ Captures a picture. """
        pass


def create_camera() -> Camera:
    """
    Creates a campera suitable for the current environment.

    On the Raspberri Pi, a the picamera module is used. Otherwise a stub
    implementation is used.
    """
    try:
        import picamera2 # Succeeds on Pi where libcamera is available.
    except ImportError as e:
        logger.warning(e)
        logger.warning("Pi Camera will not be used.")
        return FakeCamera()
    return PiCamera()

class PiCamera(Camera):
    """ A Camera that uses the Picamera2 module."""

    def __init__(self):
        from picamera2 import Picamera2
        self._camera = Picamera2()
        self._camera.options["quality"] = 90
        config = self._camera.create_still_configuration()
        self._camera.start(config)
    
    async def capture_picture(self) -> Picture:
        # Keep in memory, avoid writing to the SD card if not necessary.
        data = BytesIO()
        await asyncio.to_thread(self._camera.capture_file, file_output=data, format="jpeg")
        # The server expects RFC3339, which requires the timezone
        timestamp = datetime.now().astimezone()
        return Picture(timestamp, data)

class FakeCamera(Camera):
    """ A Camera that doesn't use any hardware, it creates artificial images."""

    async def capture_picture(self) -> Picture:
        timestamp = datetime.now().astimezone()
        data = await asyncio.to_thread(self._create_image, timestamp=timestamp)
        return Picture(timestamp, data)
    
    def _create_image(self, timestamp: datetime) -> BytesIO: 
        from PIL import Image, ImageDraw
        image = Image.new('RGB', (256, 128))
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), timestamp.isoformat(sep="\n"), fill="white")
        data = BytesIO()
        image.save(data, format="jpeg")
        return data
    