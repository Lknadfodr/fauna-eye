import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

def configure_logging():
    """
    Configures the logging module.
    
    Should be called before the first logging statement and before starting 
    the application.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    logging.getLogger("wildcam").setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file = Path("logs/wildcam.log")
    file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        filename=file,
        when="midnight",
        backupCount=28,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
