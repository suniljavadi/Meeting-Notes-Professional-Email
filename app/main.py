import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.config.settings import get_settings

logging.basicConfig(level=get_settings().log_level)
logger = logging.getLogger(__name__)
app = FastAPI(title=get_settings().app_name, version="1.0.0")
app.include_router(router, prefix="/api/v1")


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started = time.perf_counter()
    request_id = request.headers.get("X-Request-ID", "generated")
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info("request_id=%s method=%s path=%s status=%s duration_ms=%.2f", request_id, request.method, request.url.path, response.status_code, (time.perf_counter() - started) * 1000)
        return response
    except Exception:
        logger.exception("request_id=%s path=%s failed", request_id, request.url.path)
        raise


@app.get("/health")
def health():
    return {"status": "ok", "environment": get_settings().environment}


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
