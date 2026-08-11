from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ApiResponse[T](BaseModel):
    data: T | None = None
    error: ErrorDetail | None = None
