from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.health.router import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Ticket Management API",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix="/api/v1",
)
