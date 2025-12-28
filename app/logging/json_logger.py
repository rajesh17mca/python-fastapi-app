import logging
import logging.handlers
import sys
import json
from datetime import datetime
from app.logging.logging_context import FastAPILogContextFilter
from logging.handlers import RotatingFileHandler
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "event": getattr(record, "event", None),
            "txn_id": getattr(record, "txn_id", None),
            "uri": getattr(record, "uri", None),
            "time_taken_ms": getattr(record, "time_taken_ms", None),
            "message": record.getMessage(),
            "path": f"{record.pathname}:{record.lineno}",
            "func": record.funcName,
        }

        if hasattr(record, "extra_info") and record.extra_info:
            log_record["extra"] = record.extra_info

        log_record = {k: v for k, v in log_record.items() if v is not None}
        return json.dumps(log_record)

def setup_logger(logger_name="fastapi_app", log_file="app.log", console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = JsonFormatter()

    file_handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
    file_handler.setFormatter(formatter)

    file_handler.addFilter(FastAPILogContextFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    stream_handler.addFilter(FastAPILogContextFilter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger