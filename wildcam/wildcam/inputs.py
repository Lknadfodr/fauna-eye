import logging
logger = logging.getLogger(__name__)

import asyncio
from wildcam.config import Config
from wildcam.controller import Controller
from prompt_toolkit import Application as PromptApp
from prompt_toolkit.key_binding import KeyBindings

class Inputs:
    """
    This class abstracts from the GPIO inputs.
    """

    async def run():
        """ Starts the background task that processes input events."""
        pass

def create_inputs(config: Config, controller: Controller) -> list[Inputs]:
    """
    Creates Inputs based on the current environment.
    
    On the Raspberry Pi, GPIOs and key inputs from stdin are used, otherwise
    only key inputs are used. The RPi also provides key input for remote
    control. Eventually I'll replace that with HTTP.
    """
    inputs = [KeyInputs(controller)]
    try:
        import RPi # Only available on the Pi.
    except ImportError as e:
        logger.warning(e)
        logger.warning("GPIOs will not be used.")
    else:
        inputs.append(GpioInputs(config, controller))
    return inputs

class BaseInputs(Inputs):
    def __init__(self, controller: Controller):
        self._controller = controller
        self._loop = asyncio.get_running_loop()

    def _handle_coro(self, coro):
        async def _try():
            try:
                await coro
            except Exception as e:
                logger.exception(e)
        asyncio.run_coroutine_threadsafe(_try(), self._loop)

    def _handle_async(self, callback):
        def _try():
            try:
                callback()
            except Exception as e:
                logger.exception(e)
        self._loop.call_soon_threadsafe(_try)


class GpioInputs(BaseInputs):
    def __init__(self, config: Config, controller: Controller):
        super().__init__(controller)
        from gpiozero import Button
        self._key1  = Button(pin=config.gpio_key1)
        self._key2  = Button(pin=config.gpio_key2)
        self._key3  = Button(pin=config.gpio_key3)
        self._up    = Button(pin=config.gpio_up)
        self._down  = Button(pin=config.gpio_down)
        self._left  = Button(pin=config.gpio_left)
        self._right = Button(pin=config.gpio_right)
        self._press = Button(pin=config.gpio_press)

        self._key1.when_pressed = self.on_key1_pressed
        self._key3.when_pressed = self.on_key3_pressed

    def on_key1_pressed(self):
        logger.debug("Pressed Key1.")
        self._handle_coro(self._controller.capture_picture())
    
    def on_key3_pressed(self):
        logger.debug("Pressed Key3.")
        self._handle_coro(self._controller.clear_display())


class KeyInputs(BaseInputs):
    def __init__(self, controller: Controller):
        super().__init__(controller)
        kb = KeyBindings()

        @kb.add('1')
        def _(event):
            self._handle_coro(controller.capture_picture())

        @kb.add('3')
        def _(event):
           self._handle_coro(controller.clear_display())

        self._prompt = PromptApp(key_bindings=kb)

    async def run(self):
        await self._prompt.run_async()