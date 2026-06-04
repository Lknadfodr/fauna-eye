from dataclasses import dataclass
from pathlib import Path
from PIL.Image import Image

@dataclass
class Config:
    image_dir: Path

class Camera:
    """ Interface for the Picamera2. 
    
        The import statement for the picamera2 module raises in virtual 
        environments. One can use a system-site-packages venv and install
        python-libcamera, but I chose to hide the import behind an interface.
    """
    
    def capture_image(self) -> Image:
        pass


