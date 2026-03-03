import logging
from CORE.LOGGING.formatters import PipelineFormatter, DEFAULT_FORMAT
from CORE.LOGGING.handlers import get_console_handler, get_file_handler
from CORE.LOGGING.PipelineLoggerAdapter import PipelineLoggerAdapter

def get_logger(
    name: str,
    pipeline: str = "GLOBAL",
    log_file: str | None = None
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = PipelineFormatter(DEFAULT_FORMAT)

    console_handler = get_console_handler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = get_file_handler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger = PipelineLoggerAdapter(
        logger,
        extra={"pipeline": pipeline}
    )

    return logger
