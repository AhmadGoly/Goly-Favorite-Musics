import requests
import pandas as pd
import time

class MusicBrainzFetcher:
    def __init__(self):
        self.base_url = "https://musicbrainz.org/ws/2"
        self.headers = {"User-Agent": "MusicFetcher/1.0 (email@example.com)"}

    def fetch_artist_mbid(self, artist_name):
        url = f"{self.base_url}/artist"
        params = {
            "query": f'artist:"{artist_name}"',
            "fmt": "json",
            "limit": 1
        }
        response = requests.get(url, params=params, headers=self.headers)
        data = response.json()
        if data["artists"]:
            return data["artists"][0]["id"]
        return None

    def fetch_release_groups(self, mbid):
        url = f"{self.base_url}/release-group"
        params = {
            "artist": mbid,
            "fmt": "json",
            "limit": 100,
            "type": "album|single|ep"
        }
        release_groups = []
        offset = 0
        while True:
            params["offset"] = offset
            response = requests.get(url, params=params, headers=self.headers)
            data = response.json()
            release_groups.extend(data.get("release-groups", []))
            if len(data.get("release-groups", [])) < 100:
                break
            offset += 100
            time.sleep(1)
        return release_groups

    def fetch_releases_and_tracks(self, release_group_id):
        url = f"{self.base_url}/release"
        params = {
            "release-group": release_group_id,
            "fmt": "json",
            "limit": 1
        }
        response = requests.get(url, params=params, headers=self.headers)
        data = response.json()
        if not data.get("releases"):
            return []
        release_id = data["releases"][0]["id"]
        release_date = data["releases"][0].get("date", "")
        url = f"{self.base_url}/release/{release_id}"
        params = {
            "fmt": "json",
            "inc": "recordings"
        }
        response = requests.get(url, params=params, headers=self.headers)
        data = response.json()
        result = []
        for medium in data.get("media", []):
            for track in medium.get("tracks", []):
                result.append({
                    "track_title": track["title"],
                    "album_title": data.get("title", ""),
                    "release_date": release_date
                })
        time.sleep(1)
        return result

    def fetch_artist_tracks(self, artist_name):
        mbid = self.fetch_artist_mbid(artist_name)
        if not mbid:
            return pd.DataFrame()
        release_groups = self.fetch_release_groups(mbid)
        all_tracks = []
        for rg in release_groups:
            tracks = self.fetch_releases_and_tracks(rg["id"])
            all_tracks.extend(tracks)
        df = pd.DataFrame(all_tracks)
        return df
