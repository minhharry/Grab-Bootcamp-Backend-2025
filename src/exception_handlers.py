from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from models import ApiResponse 



def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Custom handler for FastAPI/Starlette HTTP exceptions.
    Converts exceptions like 404, 403, 401 into standardized ApiResponse format.

    Args:
        request (Request): The incoming HTTP request object.
        exc (StarletteHTTPException): The exception raised by FastAPI.

    Returns:
        JSONResponse: Structured error response with status, message, and optional data.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            status=exc.status_code,
            message=exc.detail if isinstance(exc.detail, str) else "An unexpected error occurred.",
            data=None,
            metadata=None
        ).model_dump(exclude_none=True)
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Custom handler for request validation errors (e.g., missing parameters, type mismatches).
    Converts 422 errors into ApiResponse with detailed error list in `data`.

    Args:
        request (Request): The incoming HTTP request object.
        exc (RequestValidationError): Validation error raised by FastAPI/Pydantic.

    Returns:
        JSONResponse: Structured error response with details about invalid fields.
    """
    return JSONResponse(
        status_code=422,
        content=ApiResponse(
            status=422,
            message="Input validation failed",
            data=exc.errors(),  # Includes location, message, and error type
            metadata=None
        ).model_dump(exclude_none=True)
    )


def internal_server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected internal errors.
    Ensures that even unhandled exceptions return a consistent response format.

    Args:
        request (Request): The incoming HTTP request object.
        exc (Exception): Any unexpected exception.

    Returns:
        JSONResponse: Structured 500 Internal Server Error response.
    """
    return JSONResponse(
        status_code=500,
        content=ApiResponse(
            status=500,
            message="Internal server error",
            data=None,
            metadata=None
        ).model_dump(exclude_none=True)
    )