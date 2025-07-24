import requests
import time
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger("MusicBrainzFetcher")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
logger.addHandler(handler)

class MusicBrainzFetcher:
    def __init__(self, rate_limit=1.0):
        self.base_url = "https://musicbrainz.org/ws/2"
        self.rate = rate_limit

    def _get(self, endpoint, params):
        time.sleep(self.rate)
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, params=params, headers={"User-Agent": "MusicFetcher/1.0 (test@example.com)"})
        res.raise_for_status()
        return res.json()

    def search_artist_mbid(self, name):
        logger.info(f"Searching artist: {name}")
        js = self._get("artist", {"query": name, "fmt": "json"})
        if not js.get("artists"):
            raise ValueError("Artist not found")
        mbid = js["artists"][0]["id"]
        logger.info(f"MBID: {mbid}")
        return mbid

    def fetch_all_releases(self, mbid):
        logger.info(f"Browse releases: {mbid}")
        releases, offset = [], 0
        while True:
            js = self._get("release", {
                "artist": mbid,
                "fmt": "json",
                "limit": 100,
                "offset": offset,
                "inc": "recordings+media"
            })
            batch = js.get("releases", [])
            releases.extend(batch)
            logger.info(f"{len(batch)} releases @offset {offset}")
            if len(batch) < 100:
                break
            offset += 100
        logger.info(f"{len(releases)} total releases")
        return releases

    def normalize_date(self, date_str):
        if not date_str:
            return "unknown"
        try:
            parsed = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed.date().isoformat()
        except:
            try:
                parsed = datetime.strptime(date_str, "%Y-%m")
                return parsed.date().isoformat()
            except:
                try:
                    parsed = datetime.strptime(date_str, "%Y")
                    return parsed.date().isoformat()
                except:
                    return "unknown"

    def fetch_tracks_with_dates(self, releases):
        rows = []
        for idx, r in enumerate(releases):
            raw_date = r.get("date")
            date = self.normalize_date(raw_date)
            for media in r.get("media", []):
                for track in media.get("tracks", []):
                    rows.append({
                        "track_title": track["title"],
                        "recording_id": track["recording"]["id"],
                        "release_id": r["id"],
                        "release_date": date
                    })
        return rows

    def fetch_artist_tracks_df(self, artist_name):
        logger.info(f"Starting fetch for artist: {artist_name}")
        mbid = self.search_artist_mbid(artist_name)
        releases = self.fetch_all_releases(mbid)
        data = self.fetch_tracks_with_dates(releases)
        df = pd.DataFrame(data)
        df["sort_date"] = df["release_date"].apply(lambda x: x if x != "unknown" else "9999-12-31")
        df = df.sort_values("sort_date", ascending=False).drop(columns="sort_date").reset_index(drop=True)
        logger.info(f"Created DataFrame with {len(df)} rows")
        return df
