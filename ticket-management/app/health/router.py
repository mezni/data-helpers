from fastapi import APIRouter

from app.core.config import settings
from app.core.mongodb_health import check_mongodb_health


router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


@router.get(
    "/health/mongodb",
    summary="Check MongoDB health",
    tags=["Health"],
)
async def mongodb_health_check() -> dict[str, str]:
    await check_mongodb_health()

    return {
        "status": "healthy",
        "database": settings.mongodb_database,
    }
