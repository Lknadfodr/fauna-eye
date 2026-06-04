import logging
logger = logging.getLogger(__name__)

from common import Config, Camera
from display import Display
from datetime import datetime
from uuid import uuid4

class Application:
    """ This class contains most of the business logic, i.e. capturing images, 
        uploading them to the server and updating the display. 
    """
    def __init__(self, config: Config, camera: Camera, display: Display):
        self.config = config
        self.camera = camera
        self.display = display

    def capture_image(self):
        logger.info("Capturing image ...")
        now = datetime.now()
        image = self.camera.capture_image()
        nowstr = now.strftime("%Y-%m-%d_T_%H-%M-%S")
        id = str(uuid4())
        dst = self.config.image_dir.joinpath(f"{nowstr}_{id}.jpg")
        image.save(
            fp=dst,
            format="JPEG",
            quality=90,
            optimize=True,
            progressive=False)
        self.display.show_message(now)
        logger.info("Capturing image ... done")

