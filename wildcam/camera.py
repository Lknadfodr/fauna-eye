from PIL import Image
from common import Camera
from picamera2 import Picamera2

class PiCamera(Camera):
    """ A Camera that uses the Picamera2 module."""

    def __init__(self):
        self._camera = Picamera2()
        config = self._camera.create_still_configuration()
        self._camera.start(config)
    
    def capture_image(self) -> Image:
        return self._camera.capture_image()
