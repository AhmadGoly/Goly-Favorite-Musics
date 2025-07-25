import pandas as pd
from .artist_config import ArtistConfig
from .musicbrainz_fetcher import MusicBrainzFetcher
import logging

logger = logging.getLogger("ArtistSongManager")
logging.basicConfig(level=logging.INFO)


class ArtistSongManager:
    def __init__(self, env_path=".env"):
        self.config = ArtistConfig(env_path)
        self.fetcher = MusicBrainzFetcher()

    def fetch_all_songs(self, category_or_artist=None, limit_per_artist=10):
        artists = self.config.get_artists(category_or_artist)
        logger.info(f"Fetching songs for: {artists}")
        all_rows = []

        for artist in artists:
            try:
                df = self.fetcher.fetch_artist_tracks_df(artist, limit_per_artist)
                df["artist"] = artist
                all_rows.append(df)
            except Exception as e:
                logger.warning(f"Failed to fetch for {artist}: {e}")

        if not all_rows:
            logger.warning("No data fetched.")
            return pd.DataFrame()

        final_df = pd.concat(all_rows).reset_index(drop=True)
        logger.info(f"Fetched total {len(final_df)} tracks for {len(artists)} artist(s)")
        return final_df
