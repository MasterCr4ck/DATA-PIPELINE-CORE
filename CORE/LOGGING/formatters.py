import logging

DEFAULT_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(pipeline)s | %(stage)s | %(message)s"
)

class PipelineFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "pipeline"):
            record.pipeline = "GLOBAL"
        if not hasattr(record, "stage"):
            record.stage = "-"
        return super().format(record)
