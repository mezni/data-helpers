from fastapi import APIRouter

from app.core.config import settings


router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    description="Returns the current API service status.",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
