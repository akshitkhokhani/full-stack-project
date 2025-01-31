from typing import List, Optional, Tuple
from fastapi import HTTPException
from app.models.song import Song
from app.utils.data_processor import DataProcessor
from app.core.config import settings

class SongService:
    def __init__(self):
        self.data_processor = DataProcessor()

    async def get_songs_paginated(
        self, 
        page: int = 1, 
        size: int = settings.DEFAULT_PAGE_SIZE
    ) -> Tuple[List[Song], int]:
        """
        Get paginated songs with total count
        """
        if page < 1:
            raise HTTPException(status_code=400, detail="Page number must be greater than 0")
        
        if size > settings.MAX_PAGE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"Page size cannot exceed {settings.MAX_PAGE_SIZE}"
            )

        songs, total = self.data_processor.get_paginated_songs(page, size)
        return songs, total

    async def get_song_by_title(self, title: str) -> Song:
        """
        Get a specific song by title
        """
        song = self.data_processor.get_song_by_title(title)
        if not song:
            raise HTTPException(status_code=404, detail=f"Song with title '{title}' not found")
        return song

    async def update_song_rating(self, title: str, rating: int) -> Song:
        """
        Update song rating
        """
        if not 1 <= rating <= 5:
            raise HTTPException(
                status_code=400, 
                detail="Rating must be between 1 and 5"
            )

        song = self.data_processor.update_song_rating(title, rating)
        if not song:
            raise HTTPException(status_code=404, detail=f"Song with title '{title}' not found")
        return song