from movie_analysis.tmdb_client import TMDBClient

client = TMDBClient()
movies = client.trending("day")

print(f"Fetched {len(movies)} trending movies\n")
for i, m in enumerate(movies[:5], start=1):
    year = m.get("release_date", "")[:4] or "????"
    print(f"{i}. {m['title']} ({year})  rating={m['vote_average']:.1f}  votes={m['vote_count']}")