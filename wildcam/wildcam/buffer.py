import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from wildcam.common import Picture
from wildcam.client import Client

class Buffer:
    """ Buffers pictures if the upload is currently not possible. """
    
    async def add(self, picture: Picture):
        """ Adds a picture to be uploaded. """
        pass
    
    async def retry(self):
        """ Retries to upload all currently buffered images. """
        pass

    def size(self) -> int:
        """ Returns the current amount of buffered images. """
        pass

class FileBuffer(Buffer):
    """ A Buffer that temporarily stores images as files. """
    def __init__(self, client: Client, dir: Path):
        self._client = client
        self._dir = dir
        dir.mkdir(parents=True, exist_ok=True)
        self._files = [p for p in dir.iterdir() if FileBuffer._is_buffered_file(p)]

    _TIME_FORMAT = "%Y-%m-%d_%H-%M-%S.%f+%z"

    def _try_strptime(string: str):
        try:
            return datetime.strptime(string, FileBuffer._TIME_FORMAT)
        except:
            return None

    def _is_buffered_file(path: Path):
        return path.is_file() \
            and path.suffix == ".jpg" \
            and FileBuffer._try_strptime(path.stem)
    
    async def add(self, picture: Picture):
        # Try immediate upload first. Only if it fails save to file,
        # to avoid SD card writing.
        status = await self._client.upload(picture)
        if status == HTTPStatus.OK:
            return
        timestr = picture.timestamp.strftime(FileBuffer._TIME_FORMAT)
        file = self._dir.joinpath(timestr + ".jpg")
        with open(file, "wb") as writer:
            writer.write(picture.image.getvalue())
        self._files.append(file)
    
    #async def _store_image():


    async def retry(self):
        remaining = []
        for f in self._files:
            timestamp = datetime.strptime(f.stem, FileBuffer._TIME_FORMAT)
            with open(f, "rb") as image:
                picture = Picture(timestamp, image)
                status = await self._client.upload(picture)
            if status == HTTPStatus.OK:
                f.unlink()
            else:
                remaining.append(f)
        self._files = remaining

    def size(self):
        return len(self._files)
