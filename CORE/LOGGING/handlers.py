import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_console_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    return handler

def get_file_handler(log_path="logs/pipeline.log"):
    # Convertimos a Path
    log_path = Path(log_path)

    # Creamos carpeta si no existe
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=10_000_000,
        backupCount=5
    )
    handler.setLevel(logging.INFO)

    return handler