import json
import pandas as pd
from typing import List, Optional, Tuple
from app.models.song import Song
from app.core.config import settings

class DataProcessor:
    def __init__(self, json_file_path: str = settings.DATA_FILE_PATH):
        self.json_file_path = json_file_path
        self.normalized_data: List[Song] = []
        self._load_and_normalize_data()

    def _load_and_normalize_data(self) -> None:
        """Load and normalize the JSON data into Song objects"""
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(data)
            
            # Normalize the data
            for idx in df.index:
                str_idx = str(idx)
                song_dict = {
                    'index': idx,
                    'id': df['id'][str_idx],
                    'title': df['title'][str_idx],
                    'danceability': df['danceability'][str_idx],
                    'energy': df['energy'][str_idx],
                    'key': df['key'][str_idx],
                    'loudness': df['loudness'][str_idx],
                    'mode': df['mode'][str_idx],
                    'acousticness': df['acousticness'][str_idx],
                    'instrumentalness': df['instrumentalness'][str_idx],
                    'liveness': df['liveness'][str_idx],
                    'valence': df['valence'][str_idx],
                    'tempo': df['tempo'][str_idx],
                    'duration_ms': df['duration_ms'][str_idx],
                    'time_signature': df['time_signature'][str_idx],
                    'num_bars': df['num_bars'][str_idx],
                    'num_sections': df['num_sections'][str_idx],
                    'num_segments': df['num_segments'][str_idx]
                }
                self.normalized_data.append(Song(**song_dict))
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")

    def get_paginated_songs(
        self, 
        page: int = 1, 
        size: int = settings.DEFAULT_PAGE_SIZE
    ) -> Tuple[List[Song], int]:
        """Get a paginated list of songs"""
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        return (
            self.normalized_data[start_idx:end_idx],
            len(self.normalized_data)
        )

    def get_song_by_title(self, title: str) -> Optional[Song]:
        """Get a song by its title"""
        for song in self.normalized_data:
            if song.title.lower() == title.lower():
                return song
        return None

    def update_song_rating(self, title: str, rating: int) -> Optional[Song]:
        """Update the rating of a song"""
        song = self.get_song_by_title(title)
        if song:
            song.rating = rating
            return song
        return None