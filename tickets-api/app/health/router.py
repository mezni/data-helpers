from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    tags=["Health"],
)
async def health_check() -> dict:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
