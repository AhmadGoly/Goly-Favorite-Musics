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
        self.rate = 1

    def _get(self, path, params):
        time.sleep(self.rate)
        return requests.get(f"{self.base}/{path}", params=params, headers=self.headers).json()

    def fetch_artist_mbid(self, name):
        logger.info(f"Searching artist: {name}")
        js = self._get("artist", {"query": f'artist:"{name}"', "fmt": "json", "limit": 1})
        if artists := js.get("artists"):
            mbid = artists[0]["id"]
            logger.info(f"MBID: {mbid}")
            return mbid
        logger.warning("Not found")
        return None

    def fetch_all_releases(self, mbid):
        logger.info(f"Browse releases: {mbid}")
        releases, ofs = [], 0
        while True:
            js = self._get("release", {
                "artist": mbid,
                "fmt": "json",
                "limit": 100,
                "offset": ofs,
                "inc": "release-groups"
            })
            batch = js.get("releases", [])
            releases.extend(batch)
            logger.info(f"{len(batch)} releases @offset {ofs}")
            if len(batch) < 100:
                break
            ofs += 100
        logger.info(f"{len(releases)} total releases")
        return releases

    def fetch_tracks_with_dates(self, releases):
        rows = []
        for idx, r in enumerate(releases):
            rid, date = r["id"], r.get("date")
            if not date:
                continue
            logger.info(f"[{idx+1}/{len(releases)}] Fetching release: {rid} ({date})")
            try:
                js = self._get(f"release/{rid}", {"fmt": "json", "inc": "recordings"})
                for m in js.get("media", []):
                    for t in m.get("tracks", []):
                        rows.append({
                            "track_title": t["title"],
                            "recording_id": t["recording"]["id"],
                            "release_id": rid,
                            "release_date": date
                        })
            except Exception as e:
                logger.warning(f"Failed to fetch release {rid}: {e}")
        return rows


    def fetch_artist_tracks(self, name):
        mbid = self.fetch_artist_mbid(name)
        if not mbid:
            return pd.DataFrame()
        releases = self.fetch_all_releases(mbid)
        rows = self.fetch_tracks_with_dates(releases)
        df = pd.DataFrame(rows)
        logger.info(f"{len(df)} tracks with dates")
        return df
