export async function handleNewSongs(artistName) {
    const headers = {
      'User-Agent': 'TrackifyBot/1.0 (contact@example.com)'
    };
  
    async function delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  
    async function fetchJSON(endpoint, params) {
      const url = new URL(`https://musicbrainz.org/ws/2/${endpoint}`);
      params.fmt = "json";
      Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, v));
      await delay(1000); // Rate limit
      const res = await fetch(url, { headers });
      if (!res.ok) throw new Error(`Failed request to ${endpoint}`);
      return res.json();
    }
  
    async function searchMBID(name) {
      const data = await fetchJSON("artist", { query: name });
      if (!data.artists || data.artists.length === 0) throw new Error("Artist not found");
      return data.artists[0].id;
    }
  
    async function fetchReleases(mbid) {
      let releases = [], offset = 0;
      while (true) {
        const data = await fetchJSON("release", {
          artist: mbid,
          inc: "recordings+media",
          limit: 100,
          offset
        });
        releases = releases.concat(data.releases || []);
        if (!data.releases || data.releases.length < 100) break;
        offset += 100;
      }
      return releases;
    }
  
    function normalizeDate(dateStr) {
      if (!dateStr) return "unknown";
      try {
        return new Date(dateStr).toISOString().split("T")[0];
      } catch {
        return "unknown";
      }
    }
  
    function extractTracks(releases) {
      const rows = [];
      for (const release of releases) {
        const releaseDate = normalizeDate(release.date);
        for (const media of (release.media || [])) {
          for (const track of (media.tracks || [])) {
            rows.push({
              title: track.title,
              releaseDate
            });
          }
        }
      }
      return rows;
    }
  
    try {
      const mbid = await searchMBID(artistName);
      const releases = await fetchReleases(mbid);
      const tracks = extractTracks(releases);
  
      const seen = new Set();
      const sorted = tracks
        .filter(t => {
          if (seen.has(t.title)) return false;
          seen.add(t.title);
          return true;
        })
        .sort((a, b) => {
          const d1 = a.releaseDate === "unknown" ? "9999-12-31" : a.releaseDate;
          const d2 = b.releaseDate === "unknown" ? "9999-12-31" : b.releaseDate;
          return d2.localeCompare(d1);
        });
  
      const top10 = sorted.slice(0, 10);
      return top10.map((t, i) => `${i + 1}. ${t.title} (${t.releaseDate})`).join("\n");
  
    } catch (err) {
      return `Error fetching songs: ${err.message}`;
    }
  }
  