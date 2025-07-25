import os
import pandas as pd
from .artist_song_manager import ArtistSongManager
import logging

logger = logging.getLogger("NewSongTracker")
logging.basicConfig(level=logging.INFO)


class NewSongTracker:
    def __init__(self, storage_path="data/songs_history.csv"):
        self.manager = ArtistSongManager()
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    def _load_previous(self):
        if os.path.exists(self.storage_path):
            logger.info("Loading previous song data")
            return pd.read_csv(self.storage_path)
        logger.info("No previous data found, assuming first run")
        return pd.DataFrame(columns=["track_title", "release_date", "artist"])

    def _save_updated(self, updated_df):
        updated_df.to_csv(self.storage_path, index=False)
        logger.info(f"Saved updated dataset with {len(updated_df)} total rows")

    def find_new_songs(self, category_or_artist=None, limit_per_artist=10):
        old_df = self._load_previous()
        new_df = self.manager.fetch_all_songs(category_or_artist, limit_per_artist)

        if old_df.empty:
            logger.info("First run: returning all fetched songs as new")
            self._save_updated(new_df)
            return new_df

        merged_df = pd.concat([old_df, new_df])
        merged_df = merged_df.drop_duplicates(subset=["track_title", "release_date", "artist"], keep="first")
        new_only = pd.concat([merged_df, old_df]).drop_duplicates(keep=False)

        if not new_only.empty:
            logger.info(f"Found {len(new_only)} new song(s)")
        else:
            logger.info("No new songs found")

        self._save_updated(merged_df)
        return new_only.reset_index(drop=True)
