import logging

from wildcam.client import Client
logger = logging.getLogger(__name__)

import asyncio, socket
from datetime import datetime
from http import HTTPStatus
from wildcam.camera import Camera
from wildcam.buffer import Buffer
from wildcam.display import Display

class Controller:
    """ 
    The controller contains most of the business logic, i.e. capturing images,
    uploading them to the server and updating the display. 
    """
    def __init__(self, camera: Camera, display: Display, buffer: Buffer, client: Client):
        self._camera = camera
        self._display = display
        self._buffer = buffer
        self._client = client
        self._ip: str = ""
        self._status: HTTPStatus = None
        self._last: datetime = None

    async def run(self):
        """
        Runs the background tasks: refreshing the display and monitoring the connection.
        """
        await asyncio.gather(
            asyncio.create_task(self._loop_render()),
            asyncio.create_task(self._loop_monitor())
        )

    async def _loop_render(self):
        try :
            while True:
                self._display.render(self._ip, self._status, self._last, self._buffer.size())
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(e)
            logger.error("Exiting appliction loop.")

    async def capture_picture(self):
        """ Takes a picture and queues it to be uploaded. """
        logger.info("Capturing image ...")
        picture = await self._camera.capture_picture()
        logger.info("Capturing image ... done")
        self._last = picture.timestamp
        await self._buffer.add(picture)

    async def clear_display(self):
        """ Clears the display contents. """
        self._display.clear()

    async def _loop_monitor(self):
        try: 
            while True:
                self._ip = _get_ip()
                self._status = await self._client.health() if self._ip else None
                if self._buffer.size() and self._ip and self._status == HTTPStatus.OK:
                    await self._buffer.retry()
                await asyncio.sleep(30)
        except Exception as e:
            logger.exception(e)
            logger.warning("Exiting monitor loop.")

def _get_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # IP doesn't matter, UDP (SOCK_DGRAM) is connectionless.
            # We're only retrieving the IP and don't send anything.
            s.connect(("9.9.9.9", 80))
            return s.getsockname()[0]
    except OSError:
        return None