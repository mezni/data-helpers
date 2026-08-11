from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError


async def application_exception_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )
