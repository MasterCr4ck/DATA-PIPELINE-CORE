import logging

class PipelineLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})

        merged = {
            "stage": "-",
            **self.extra,
            **extra
        }

        kwargs["extra"] = merged
        return msg, kwargs