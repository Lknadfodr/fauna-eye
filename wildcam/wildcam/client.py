import logging
logger = logging.getLogger(__name__)

from wildcam.common import Picture
from http import HTTPStatus
import httpx


class Client:
    """ Interface for the server connection. """

    async def upload(self, picture: Picture) -> HTTPStatus:
        """ Uploads the given image. """
        pass

    async def health(self) -> HTTPStatus:
        """ """
        pass

class HttpClient(Client):
    """ The HttpClient uses HTTP POST requests to upload images immediately. """

    def __init__(self, host_address: str):
        self.host_address = host_address

    async def upload(self, picture: Picture):
        url = f"{self.host_address}/api/images"
        # The go FormFile expects a nonempty filename, but it will be ignored eventually.
        files = { "file": ("none", picture.image, "image/jpeg")}
        data = { "timestamp": picture.timestamp.isoformat(timespec="seconds") }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, files=files, data=data)
            logger.debug(f"Upload response: ({response.status_code}) {response.text}")
            return HTTPStatus(response.status_code)
        except Exception as e:
            logger.warning(e)
            return HTTPStatus.IM_A_TEAPOT # faute de mieux
    
    async def health(self):
        url = f"{self.host_address}/health"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=2)
            return HTTPStatus(response.status_code)
        except Exception as e:
            return HTTPStatus.IM_A_TEAPOT # faute de mieux

