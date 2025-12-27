from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import html
import requests
from app.config.settings import settings

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

RESOURCE_ID = "6fc859cb-8a6f-458b-bd5a-9bd0cfbfce11"
DATASET_URL = (
    "https://data.gov.il/api/3/action/datastore_search"
    f"?resource_id={RESOURCE_ID}"
)

CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # once a week
CACHE_PATH = settings.CACHE_DIR / "_israeli_embassies_cache.json"

# ------------------------------------------------------------
# Errors
# ------------------------------------------------------------

class EmbassyServiceError(RuntimeError):
    pass

# ------------------------------------------------------------
# Cache helpers
# ------------------------------------------------------------

def _cache_is_fresh() -> bool:
    if not CACHE_PATH.exists():
        return False

    age = time.time() - CACHE_PATH.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def _load_cache() -> List[Dict[str, Any]]:
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def _save_cache(data: List[Dict[str, Any]]) -> None:
    CACHE_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# ------------------------------------------------------------
# Fetch & normalize
# ------------------------------------------------------------

_EMAIL_RE = re.compile(r"mailto:([^\"'>\s]+)", re.IGNORECASE)
_URL_RE = re.compile(r"https?://[^\"'>\s]+", re.IGNORECASE)

def _extract_email(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    # Decode \u003C, &amp;, etc.
    value = html.unescape(value)

    match = _EMAIL_RE.search(value)
    return match.group(1) if match else None


def _extract_website(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    # Decode \u003C, &amp;, etc.
    value = html.unescape(value)

    match = _URL_RE.search(value)
    return match.group(0) if match else None


def _fetch_and_cache() -> List[Dict[str, Any]]:
    try:
        response = requests.get(DATASET_URL, timeout=20)
        response.raise_for_status()

        records = response.json()["result"]["records"]

        normalized = [
            {
                "country": r.get("shem_mdn_a"),
                "city": r.get("shem_ntz_a"),
                "type": r.get("maamad_a"),
                "address": r.get("Addrs"),
                "phone": r.get("tel"),
                "email": _extract_email(r.get("email")),
                "website": _extract_website(r.get("Atar")),
            }
            for r in records
        ]

        _save_cache(normalized)
        return normalized

    except Exception as exc:
        raise EmbassyServiceError(
            "Failed to fetch Israeli embassy contact details"
        ) from exc


# ------------------------------------------------------------
# Public domain API
# ------------------------------------------------------------

def get_israeli_embassies(
    country: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Return contact details for Israeli embassies and consulates.

    If `country` is provided, results are filtered by country name.
    """

    if _cache_is_fresh():
        embassies = _load_cache()
    else:
        embassies = _fetch_and_cache()

    if country:
        country_lower = country.lower()
        embassies = [
            e for e in embassies
            if e.get("country") and e["country"].lower() == country_lower
        ]

    return embassies


#############################

# import pprint 

# print("\n=== ISRAELI EMBASSIES DOMAIN SMOKE TEST ===\n")

# # 1️⃣ Full dataset (cached or fetched)
# all_embassies = get_israeli_embassies()

# print(f"Total embassies fetched: {len(all_embassies)}")

# if not all_embassies:
#     raise RuntimeError("No embassy data returned")

# print("\nSample entry:\n")
# print(json.dumps(all_embassies[0], indent=2, ensure_ascii=False))

# # 2️⃣ Filter by country
# country = "United States of America"
# us_embassies = get_israeli_embassies(country=country)

# print(f"\nEmbassies in {country}: {len(us_embassies)}")

# for e in us_embassies[:1]:
#     pprint.pprint(e)