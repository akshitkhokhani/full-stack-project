from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Song Analytics API"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000","*"] 
    
    # Data Configuration
    DATA_FILE_PATH: str = "playlist.json"
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()