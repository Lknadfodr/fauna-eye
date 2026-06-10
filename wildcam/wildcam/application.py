import logging
logger = logging.getLogger(__name__)

import asyncio
from wildcam.config import Config
from wildcam.camera import create_camera
from wildcam.client import HttpClient
from wildcam.display import create_display
from wildcam.controller import Controller
from wildcam.buffer import FileBuffer
from wildcam.inputs import create_inputs

class Application:
    """
    The Application is the composition root. It creates the subcomponents and
    starts background tasks.
    """
    def __init__(self, config: Config):
        camera = create_camera()
        logger.debug("Created camera.")
        self._display = create_display()
        logger.debug("Created display.")
        self._client = HttpClient(config.upload_address)
        logger.debug("Created client.")
        buffer = FileBuffer(self._client, config.image_dir)
        logger.debug("Created buffer.")
        self._controller = Controller(camera, self._display, buffer, self._client)
        logger.debug("Created controller.")
        self._inputs = create_inputs(config, self._controller)
        logger.debug("Created inputs.")

    async def run(self):
        """ Runs background tasks. When the coroutine terminates, all background tasks terminated."""
        tasks = [asyncio.create_task(self._controller.run())] +\
                [asyncio.create_task(i.run()) for i in self._inputs]
        logger.info("Application running.")
        await asyncio.gather(*tasks)
        logger.info("Application terminated.")
