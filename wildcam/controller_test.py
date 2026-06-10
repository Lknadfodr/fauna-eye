import unittest
from unittest import TestCase
from unittest.mock import create_autospec
from controller import Controller
from camera import Camera
from display import Display
from buffer import Buffer

class ControllerTest(TestCase):

    def setUp(self):
        self.config = Config(upload_address="", image_dir="/tmp")
        self.camera: Camera = create_autospec(Camera, instance=True)
        self.display: Display = create_autospec(Display, instance=True)
        self.buffer: Buffer = create_autospec(Buffer, instance=True)
        self.controller = Controller(self.camera, self.display, self.buffer)

    def test_capture_image(self):
        self.controller.capture_image()
        self.camera.capture_picture.assert_called_once()
        self.display.render.assert_called_once()

if __name__ == '__main__':
    unittest.main()
