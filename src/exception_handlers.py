from fastapi import Request, HTTPException
from common_schemas.response import ApiResponse, ErrorMetadata
from fastapi.responses import JSONResponse
from datetime import datetime

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTPException to return in the ApiResponse format.
    This includes additional metadata like timestamp.
    """
    error_metadata = ErrorMetadata(
        timestamp=datetime.now().isoformat(),
        path=str(request.url)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            status=exc.status_code,
            message=exc.detail if isinstance(exc.detail, str) else "An unexpected error occurred",
            data=None,
            metadata=error_metadata
        ).model_dump()
    )
