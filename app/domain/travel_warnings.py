import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
import sys
from app.config.settings import settings
sys.stdout.reconfigure(encoding="utf-8")

"""
Domain logic for travel warnings using Israeli government API.
Fetches travel warnings with daily caching and provides recommendations per country.
"""

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
RESOURCE_ID = "2a01d234-b2b0-4d46-baa0-cec05c401e7d"
DATASET_URL = settings.GOV_IL_API_URL + f"?resource_id={RESOURCE_ID}"
DATASET_LIMIT = 32000

CACHE_FILE = settings.CACHE_DIR / "travel_warnings_cache.json"
BASE_FILE = settings.DATA_DIR / "country_en_to_he.json"
CACHE_TTL = timedelta(days=1)

# ---------------------------------------------------------------------
# Load English -> Hebrew country mapping
# ---------------------------------------------------------------------
with open(BASE_FILE, encoding="utf-8") as f:
    COUNTRY_EN_TO_HE = json.load(f)

# ---------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------
def is_cache_fresh(path: Path, ttl: timedelta) -> bool:
    if not path.exists():
        return False
    modified_time = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - modified_time < ttl

# ---------------------------------------------------------------------
# Fetch from API
# ---------------------------------------------------------------------
def fetch_travel_warnings_from_api() -> list[dict]:
    response = requests.get(
        DATASET_URL,
        params={
            "resource_id": RESOURCE_ID,
            "limit": DATASET_LIMIT,
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["result"]["records"]

# ---------------------------------------------------------------------
# Load records with daily cache + fallback
# ---------------------------------------------------------------------
def load_travel_warnings() -> list[dict]:
    # Fresh cache → use it
    if is_cache_fresh(CACHE_FILE, CACHE_TTL):
        with CACHE_FILE.open(encoding="utf-8") as f:
            return json.load(f)

    # Cache missing or stale → try API
    try:
        records = fetch_travel_warnings_from_api()
        with CACHE_FILE.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False)
        return records

    # API failed → fallback to any existing cache
    except Exception:
        if CACHE_FILE.exists():
            with CACHE_FILE.open(encoding="utf-8") as f:
                return json.load(f)
        raise  # no cache and no API → hard fail

# ---------------------------------------------------------------------
# Load records once (cached)
# ---------------------------------------------------------------------
RECORDS = load_travel_warnings()

# ---------------------------------------------------------------------
# Public API: recommendations only
# ---------------------------------------------------------------------
def fetch_travel_warnings(country_en: str) -> set[str]:

    # 1. Fast deterministic path
    hebrew = COUNTRY_EN_TO_HE.get(country_en.strip().lower())

    # 2. Fail safe
    if not hebrew:
        return set()

    return {
        r["recommendations"]
        for r in RECORDS
        if r.get("country") == hebrew and r.get("recommendations")
    }