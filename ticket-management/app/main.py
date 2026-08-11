from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.comments.router import router as comments_router
from app.core.config import settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.health.router import router as health_router
from app.tickets.router import router as tickets_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Ticket Management API - Modular Monolith",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)


app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    users_router,
    prefix="/api/v1/admin/users",
    tags=["Admin - Users"],
)

app.include_router(
    tickets_router,
    prefix="/api/v1/tickets",
    tags=["Tickets"],
)

app.include_router(
    comments_router,
    prefix="/api/v1/tickets",
    tags=["Comments"],
)
