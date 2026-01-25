import logging


class SafeRequestIdFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return super().format(record)


def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        SafeRequestIdFormatter("%(asctime)s %(levelname)s request_id=%(request_id)s %(message)s")
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
