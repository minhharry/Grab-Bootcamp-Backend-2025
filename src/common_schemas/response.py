from pydantic import BaseModel
from typing import Optional, Any

class Metadata(BaseModel):
    """
    Metadata for paginated responses.
    Included only when the API returns paginated data.
    """
    page: Optional[int] = None
    size: Optional[int] = None
    total: Optional[int] = None

class ApiResponse(BaseModel):
    """
    Standard structure for all API responses.

    Attributes:
        status (int): HTTP status code
        message (str): Human-readable message
        data (Any): Actual payload of the response
        metadata (Metadata | None): Optional metadata for pagination or other context
    """
    status: int
    message: str
    data: Optional[Any] = None
    metadata: Optional[Metadata] = None
