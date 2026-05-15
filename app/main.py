import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.users.router import router as users_router
from app.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application...")
    async with engine.begin() as conn:
        # In production, use migrations (Alembic) instead of create_all
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Stefanini User Management API",
    description="RESTful API for user management with complete CRUD operations.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    # Provide a cleaner response for bad UUIDs in the path.
    for err in errors:
        loc = err.get("loc", [])
        msg = err.get("msg", "")
        if "user_id" in loc and "UUID" in msg:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid user_id"},
            )

    formatted_errors = []
    for err in errors:
        field = ".".join(str(loc) for loc in err.get("loc", []))
        message = err.get("msg", "Invalid input")
        formatted_errors.append(f"{field}: {message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Data validation failed",
            "errors": formatted_errors,
        },
    )

app.include_router(users_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
