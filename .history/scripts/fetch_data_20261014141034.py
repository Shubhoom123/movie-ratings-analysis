"""Fetch movies from TMDB by release year and save to data/raw."""
import argparse

import pandas as pd

from movie_analysis.config import DATA_RAW
from movie_analysis.tmdb_client import TMDBClient


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=2000)
    p.add_argument("--end", type=int, default=2025)
    p.add_argument("--max-pages", type=int, default=25)
    args = p.parse_args()

    client = TMDBClient()
    rows = []
    for year in range(args.start, args.end + 1):
        year_rows = client.discover_year(year, max_pages=args.max_pages)
        print(f"{year}: {len(year_rows)} movies")
        rows.extend(year_rows)

    DATA_RAW.mkdir(parents=True, exist_ok=True)

    movies = pd.DataFrame(rows)
    movies.to_parquet(DATA_RAW / "movies.parquet", index=False)

    genres = pd.DataFrame(list(client.genres().items()), columns=["id", "name"])
    genres.to_parquet(DATA_RAW / "genres.parquet", index=False)

    print(f"\nSaved {len(movies):,} movies, shape {movies.shape}")
    print(movies[["title", "release_date", "vote_average", "vote_count", "popularity"]].head())


if __name__ == "__main__":
    main()