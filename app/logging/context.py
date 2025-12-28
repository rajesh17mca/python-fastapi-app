from contextvars import ContextVar

request_context = ContextVar(
    "request_context",
    default={
        "txn_id": None,
        "uri": None,
        "time_taken_ms": None,
    },
)