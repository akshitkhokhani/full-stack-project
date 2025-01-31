from pydantic import BaseModel
from typing import List, Optional
from app.models.song import Song

class PaginatedResponse(BaseModel):
    """Schema for paginated responses"""
    items: List[Song]
    total: int
    page: int
    size: int
    pages: int

class RatingUpdate(BaseModel):
    """Schema for rating update requests"""
    rating: int

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str