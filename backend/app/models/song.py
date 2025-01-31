from pydantic import BaseModel, Field
from typing import Optional

class SongBase(BaseModel):
    """Base Song model with common attributes"""
    id: str
    title: str
    danceability: float = Field(ge=0, le=1)
    energy: float = Field(ge=0, le=1)
    key: int = Field(ge=0, le=11)
    loudness: float
    mode: int = Field(ge=0, le=1)
    acousticness: float = Field(ge=0, le=1)
    instrumentalness: float = Field(ge=0, le=1)
    liveness: float = Field(ge=0, le=1)
    valence: float = Field(ge=0, le=1)
    tempo: float
    duration_ms: int
    time_signature: int
    num_bars: int
    num_sections: int
    num_segments: int

class Song(SongBase):
    """Song model with additional fields"""
    index: int
    rating: Optional[int] = Field(None, ge=1, le=5)

    class Config:
        from_attributes = True