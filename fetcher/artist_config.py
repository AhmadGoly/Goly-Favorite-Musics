import os
import json
from dotenv import load_dotenv

class ArtistConfig:
    def __init__(self, env_path=".env"):
        load_dotenv(env_path)
        raw = os.getenv("FAVORITE_ARTISTS")
        if not raw:
            raise ValueError("FAVORITE_ARTISTS not found in .env")
        self.artist_map = json.loads(raw)

    def get_artists(self, category_or_artist=None):
        if category_or_artist is None:
            return [artist for group in self.artist_map.values() for artist in group]

        if category_or_artist in self.artist_map:
            return self.artist_map[category_or_artist]

        # Treat as individual artist name
        for group in self.artist_map.values():
            if category_or_artist in group:
                return [category_or_artist]

        raise ValueError(f"No artist or class found for: {category_or_artist}")
