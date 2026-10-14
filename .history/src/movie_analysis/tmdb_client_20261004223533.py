import time
import requests
from .config import TMDB_BASE_URL, get_tmdb_token


class TMDBClient:
    def __init__(self, token=None, pause=0.1):
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {token or get_tmdb_token()}"}
        )
        self.pause = pause

    def get(self, path, **params):
        for attempt in range(5):
            r = self.session.get(f"{TMDB_BASE_URL}{path}", params=params, timeout=15)
            if r.status_code == 429:  # rate limited -> back off and retry
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            time.sleep(self.pause)
            return r.json()
        raise RuntimeError(f"Rate limited too many times on {path}")

    def trending(self, window="day"):
        return self.get(f"/trending/movie/{window}")["results"]

    def genres(self):
        data = self.get("/genre/movie/list")
        return {g["id"]: g["name"] for g in data["genres"]}

    def discover_year(self, year, max_pages=25, min_votes=50):
        """Movies released in `year`, most popular first (20 per page)."""
        rows = []
        for page in range(1, max_pages + 1):
            data = self.get(
                "/discover/movie",
                primary_release_year=year,
                sort_by="popularity.desc",
                page=page,
                **{"vote_count.gte": min_votes},
            )
            rows.extend(data["results"])
            if page >= data["total_pages"]:
                break
        return rows