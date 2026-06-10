import logging
from wildcam.logconfig import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
logger.debug("Logging configured.")

import asyncio
from wildcam.application import Application
from wildcam.config import Config

def main():
    asyncio.run(_main())
    logger.info("Exiting main thread.")

async def _main():
    config = Config.load()
    logger.info(f"Loaded configuration {config}")
    app = Application(config)
    logger.info("Created application.")
    await app.run()
