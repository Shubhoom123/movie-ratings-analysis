import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIG_DIR = ROOT / "figures"

SEED = 42
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def get_tmdb_token():
    token = os.getenv("TMDB_TOKEN")
    if not token:
        raise RuntimeError("Tok check, not set" \
        "")
    return token