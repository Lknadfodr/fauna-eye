import unittest
from unittest import TestCase
from unittest.mock import create_autospec
from pathlib import Path
from app import Application
from common import Camera, Config
from display import Display

class ApplicationTest(TestCase):

    def setUp(self):
        self.config = Config(image_dir=Path("/tmp"))
        self.camera: Camera = create_autospec(Camera, instance=True)
        self.display: Display = create_autospec(Display, instance=True)
        self.app = Application(self.config, self.camera, self.display)

    def test_capture_image(self):
        self.app.capture_image()
        self.camera.capture_image.assert_called_once()
        self.display.show_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()
