class ApplicationError(Exception):
    """Base application exception."""

    def __init__(
        self,
        code: str,
        message: str,
    ) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class NotFoundError(ApplicationError):
    """Raised when a resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
    ) -> None:
        super().__init__(code, message)


class ConflictError(ApplicationError):
    """Raised when a resource conflicts with existing state."""

    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
    ) -> None:
        super().__init__(code, message)


class ForbiddenError(ApplicationError):
    """Raised when access is forbidden."""

    def __init__(
        self,
        message: str = "Forbidden",
        code: str = "FORBIDDEN",
    ) -> None:
        super().__init__(code, message)
