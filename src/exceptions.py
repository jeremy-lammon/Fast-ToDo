from fastapi import HTTPException
from typing import Any

class AppError(HTTPException):

    def __init__(self, status_code: int, message: str, code: str | None = None, field: str | None = None):
        detail = [{"message": message, "code": code, "field": field}]
        super().__init__(status_code=status_code, detail=detail)

class ValidationError(AppError):

    def __init__(self, message: str, field: str, code: str = "VALIDATION_ERROR"):
        super().__init__(status_code=422, message=message, code=code, field=field)

class NotFoundError(AppError):

    def __init__(self, resource: str = "Resource", resource_id: Any = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id: {resource_id}"
        super().__init__(status_code=404, message=message, code="NOT_FOUND")

class ConflictError(AppError):

    def __init__(self, message: str, field: str | None = None):
        super().__init__(status_code=409, message=message, code="CONFLICT", field=field)

class UnauthorizedError(AppError):

    def __init__(self, message: str = "Authentication required"):
        super().__init__(status_code=401, message=message, code="UNAUTHORIZED")

class ForbiddenError(AppError):

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(status_code=403, message=message, code="FORBIDDEN")