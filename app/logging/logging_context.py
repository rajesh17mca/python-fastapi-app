import logging
from app.logging.context import request_context

class FastAPILogContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = request_context.get()

        record.txn_id = ctx.get("txn_id")
        record.uri = ctx.get("uri")
        record.time_taken_ms = ctx.get("time_taken_ms")

        return True