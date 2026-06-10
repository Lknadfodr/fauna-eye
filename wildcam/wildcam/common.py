from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO

@dataclass
class Picture:
    # When this pictrue was captured.
    timestamp: datetime

    # The image data. 
    # It's not a PIL.Image to avoid duplicating the data for the HTTP request.
    image: BinaryIO # Can be BytesIO or BufferedReader.

