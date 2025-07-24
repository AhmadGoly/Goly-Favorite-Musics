import requests
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MusicBrainzFetcher")

class MusicBrainzFetcher:
    def __init__(self):
        self.base = "https://musicbrainz.org/ws/2"
        self.headers = {"User-Agent": "MusicFetcher/1.0 (email@example.com)"}
        self.rate_limit = 1  # seconds

    def _get_json(self, path, params):
        time.sleep(self.rate_limit)
        resp = requests.get(f"{self.base}/{path}", params=params, headers=self.headers)
        return resp.json()

    def fetch_artist_mbid(self, name):
        logger.info(f"Searching artist: {name}")
        js = self._get_json("artist", {"query": f'artist:"{name}"', "fmt":"json", "limit":1})
        artists = js.get("artists", [])
        if artists:
            mbid = artists[0]["id"]
            logger.info(f"Found MBID: {mbid}")
            return mbid
        logger.warning("Artist not found")
        return None

    def fetch_all_recordings(self, mbid):
        logger.info(f"Fetching recordings for MBID: {mbid}")
        records = []
        limit = 100
        offset = 0
        while True:
            js = self._get_json("recording", {
                "artist": mbid,
                "fmt": "json",
                "limit": limit,
                "offset": offset
            })
            batch = js.get("recordings", [])
            records.extend(batch)
            logger.info(f"Fetched {len(batch)} recordings (offset {offset})")
            if len(batch) < limit:
                break
            offset += limit
        logger.info(f"Total recordings fetched: {len(records)}")
        return records

    def fetch_artist_tracks(self, artist_name):
        mbid = self.fetch_artist_mbid(artist_name)
        if not mbid:
            return pd.DataFrame()
        recs = self.fetch_all_recordings(mbid)
        rows = []
        for r in recs:
            rows.append({
                "track_title": r.get("title", ""),
                "length_ms": r.get("length"),
                "recording_id": r.get("id")
            })
        df = pd.DataFrame(rows)
        logger.info(f"Created DataFrame with {len(df)} rows")
        return df
