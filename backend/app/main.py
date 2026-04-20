from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.rewrite import router as rewrite_router
from app.api.routes.suggestion import router as suggestion_router
from app.core.config import get_settings
from app.core.logging_config import configure_logging, get_logger


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting enterprise-writing-assistant backend")
    yield
    logger.info("Stopping enterprise-writing-assistant backend")


app = FastAPI(
    title="Enterprise Writing Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = perf_counter()
    logger.info(
        "Request started", extra={"method": request.method, "path": request.url.path}
    )
    response = await call_next(request)
    duration_ms = round((perf_counter() - start_time) * 1000, 2)
    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    response.headers["X-Process-Time-Ms"] = str(duration_ms)
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please retry later."},
    )


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok", "service": "enterprise-writing-assistant"}


app.include_router(suggestion_router, prefix="/api", tags=["suggestion"])
app.include_router(rewrite_router, prefix="/api", tags=["rewrite"])
