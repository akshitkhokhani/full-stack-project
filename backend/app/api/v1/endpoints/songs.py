from fastapi import APIRouter, Query, Path, Depends
from typing import List
from app.models.song import Song
from app.schemas.song import PaginatedResponse
from app.services.song_service import SongService
from app.core.config import settings

router = APIRouter()

@router.get(
    "/songs/", 
    response_model=PaginatedResponse,
    summary="Get all songs with pagination"
)
async def get_songs(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Items per page"
    ),
    service: SongService = Depends(SongService)
):
    """
    Get a paginated list of songs with the following parameters:
    - **page**: Page number (starts from 1)
    - **size**: Number of items per page
    """
    songs, total = await service.get_songs_paginated(page, size)
    total_pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=songs,
        total=total,
        page=page,
        size=size,
        pages=total_pages
    )

@router.get(
    "/songs/{title}",
    response_model=Song,
    summary="Get song by title"
)
async def get_song_by_title(
    title: str = Path(..., description="The title of the song"),
    service: SongService = Depends(SongService)
):
    """
    Get a specific song by its title
    """
    return await service.get_song_by_title(title)

@router.put(
    "/songs/{title}/rating",
    response_model=Song,
    summary="Update song rating"
)
async def update_song_rating(
    title: str = Path(..., description="The title of the song"),
    rating: int = Query(..., ge=1, le=5, description="Rating value between 1 and 5"),
    service: SongService = Depends(SongService)
):
    """
    Update the rating of a song
    - **title**: Song title
    - **rating**: New rating value (1-5)
    """
    return await service.update_song_rating(title, rating)