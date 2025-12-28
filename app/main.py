import time
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import ProductionConfig
from app.logging.json_logger import setup_logger
from app.routes.api import router as api_router
from app.logging.context import request_context

config = ProductionConfig()
app = FastAPI(debug=config.DEBUG)
app.state.config = config

logger = setup_logger(
    logger_name="fastapi_app",
    log_file=config.LOG_FILE
)
app.logger = logger

def sanitize_headers(headers):
    SENSITIVE = {"authorization", "cookie", "x-api-key"}
    return {
        k: ("***" if k.lower() in SENSITIVE else v)
        for k, v in headers.items()
    }

def define_log_event(status):
    if 100 <= status < 300:
        log_level = "info"
        message = "request_completed_success"
    elif 300 <= status < 400:
        log_level = "warning"
        message = "request_redirected"
    elif 400 <= status < 500:
        log_level = "error"
        message = "client_error"
    else:
        log_level = "critical"
        message = "server_error"
    return log_level, message

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    txn_id = request.headers.get("X-Transaction-Id", str(uuid4()))
    start_time = time.perf_counter()

    token = request_context.set({"txn_id": txn_id,
        "uri": f"{request.method} {request.url.path}",
        "time_taken_ms": None,
    })

    app.logger.info("request_started", extra={
        "event": "request_started",
        "extra_info": {
            "headers": sanitize_headers(dict(request.headers)),
            "query_params": dict(request.query_params),
            "client": request.client.host if request.client else None,
        }
    })

    response = await call_next(request)
    time_taken = round((time.perf_counter() - start_time) * 1000, 2)

    request_context.set({
        "txn_id": txn_id,
        "uri": f"{request.method} {request.url.path}",
        "time_taken_ms": time_taken,
    })

    response.headers["X-Transaction-Id"] = txn_id
    log_level, message = define_log_event(int(response.status_code))
    getattr(app.logger, log_level)(
        message,
        extra={
            "event": "request_completed",
            "status_code": response.status_code,
            "log_level": log_level,
            "extra_info": {
                "status_code": response.status_code,
                "response_headers": dict(response.headers),
            },
        }
    )
    request_context.reset(token)
    return response

app.include_router(api_router, prefix="/api/v1")
