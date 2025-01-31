import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from pydantic import ValidationError
from fastapi import HTTPException

from app.main import create_application
from app.utils.data_processor import DataProcessor
from app.services.song_service import SongService
from app.models.song import Song

# -------------- Fixtures --------------
@pytest.fixture
def test_data():
    return {
        "id": {"0": "test_id_1", "1": "test_id_2"},
        "title": {"0": "Test Song 1", "1": "Test Song 2"},
        "danceability": {"0": 0.5, "1": 0.7},
        "energy": {"0": 0.6, "1": 0.8},
        "key": {"0": 1, "1": 2},
        "loudness": {"0": -5.0, "1": -4.0},
        "mode": {"0": 1, "1": 0},
        "acousticness": {"0": 0.3, "1": 0.4},
        "instrumentalness": {"0": 0.1, "1": 0.2},
        "liveness": {"0": 0.2, "1": 0.3},
        "valence": {"0": 0.4, "1": 0.5},
        "tempo": {"0": 120.0, "1": 130.0},
        "duration_ms": {"0": 200000, "1": 210000},
        "time_signature": {"0": 4, "1": 4},
        "num_bars": {"0": 100, "1": 110},
        "num_sections": {"0": 5, "1": 6},
        "num_segments": {"0": 500, "1": 550}
    }

@pytest.fixture
def test_json_path(tmp_path, test_data):
    json_file = tmp_path / "test_playlist.json"
    json_file.write_text(json.dumps(test_data))
    return str(json_file)

@pytest.fixture
def app_client():
    app = create_application()
    return TestClient(app)

@pytest.fixture
def data_processor(test_json_path):
    return DataProcessor(test_json_path)

@pytest.fixture
def song_service(data_processor):
    service = SongService()
    service.data_processor = data_processor
    return service

@pytest.fixture
def valid_song_data():
    return {
        "index": 0,
        "id": "test_id",
        "title": "Test Song",
        "danceability": 0.5,
        "energy": 0.6,
        "key": 1,
        "loudness": -5.0,
        "mode": 1,
        "acousticness": 0.3,
        "instrumentalness": 0.1,
        "liveness": 0.2,
        "valence": 0.4,
        "tempo": 120.0,
        "duration_ms": 200000,
        "time_signature": 4,
        "num_bars": 100,
        "num_sections": 5,
        "num_segments": 500
    }

# -------------- Model Tests --------------
class TestSongModel:
    def test_valid_song_creation(self, valid_song_data):
        song = Song(**valid_song_data)
        assert song.title == "Test Song"
        assert song.danceability == 0.5

    def test_invalid_song_values(self, valid_song_data):
        invalid_data = valid_song_data.copy()
        invalid_data["danceability"] = 1.5
        with pytest.raises(ValidationError):
            Song(**invalid_data)

    def test_invalid_rating_values(self, valid_song_data):
        invalid_data = valid_song_data.copy()
        invalid_data["rating"] = 6
        with pytest.raises(ValidationError):
            Song(**invalid_data)

# -------------- Data Processor Tests --------------
class TestDataProcessor:
    def test_load_and_normalize_data(self, data_processor):
        assert len(data_processor.normalized_data) == 2
        assert data_processor.normalized_data[0].title == "Test Song 1"
        assert data_processor.normalized_data[1].title == "Test Song 2"

    def test_get_paginated_songs(self, data_processor):
        songs, total = data_processor.get_paginated_songs(page=1, size=1)
        assert len(songs) == 1
        assert total == 2
        assert songs[0].title == "Test Song 1"

    def test_get_song_by_title(self, data_processor):
        song = data_processor.get_song_by_title("Test Song 1")
        assert song is not None
        assert song.title == "Test Song 1"
        assert song.id == "test_id_1"

    def test_update_song_rating(self, data_processor):
        song = data_processor.update_song_rating("Test Song 1", 5)
        assert song is not None
        assert song.rating == 5

# -------------- Service Tests --------------
class TestSongService:
    @pytest.mark.asyncio
    async def test_get_songs_paginated(self, song_service):
        songs, total = await song_service.get_songs_paginated(page=1, size=10)
        assert len(songs) == 2
        assert total == 2

    @pytest.mark.asyncio
    async def test_get_songs_paginated_invalid_page(self, song_service):
        with pytest.raises(HTTPException) as exc:
            await song_service.get_songs_paginated(page=0)
        assert exc.value.status_code == 400

    @pytest.mark.asyncio
    async def test_get_song_by_title(self, song_service):
        song = await song_service.get_song_by_title("Test Song 1")
        assert song.title == "Test Song 1"
        assert song.id == "test_id_1"

    @pytest.mark.asyncio
    async def test_get_song_by_title_not_found(self, song_service):
        with pytest.raises(HTTPException) as exc:
            await song_service.get_song_by_title("Nonexistent Song")
        assert exc.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_song_rating_invalid_rating(self, song_service):
        with pytest.raises(HTTPException) as exc:
            await song_service.update_song_rating("Test Song 1", 6)
        assert exc.value.status_code == 400

# -------------- API Endpoint Tests --------------
class TestAPIEndpoints:
    def test_health_check(self, app_client):
        response = app_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_get_songs_pagination(self, app_client):
        response = app_client.get("/api/v1/songs/?page=1&size=10")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data

    def test_get_songs_invalid_pagination(self, app_client):
        response = app_client.get("/api/v1/songs/?page=0")
        assert response.status_code == 400

    def test_get_song_by_title(self, app_client):
        response = app_client.get("/api/v1/songs/Test%20Song%201")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Song 1"

    def test_get_song_by_title_not_found(self, app_client):
        response = app_client.get("/api/v1/songs/Nonexistent%20Song")
        assert response.status_code == 404

    def test_update_song_rating(self, app_client):
        response = app_client.put("/api/v1/songs/Test%20Song%201/rating?rating=5")
        assert response.status_code == 200
        data = response.json()
        assert data["rating"] == 5

    def test_update_song_rating_invalid(self, app_client):
        response = app_client.put("/api/v1/songs/Test%20Song%201/rating?rating=6")
        assert response.status_code == 400