from __future__ import annotations
from typing import Dict, Any
import requests

"""
Domain logic for timezone service using WorldTimeAPI.
Fetches current local time and timezone metadata for a given timezone.
"""

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

WORLD_TIME_API_BASE = "http://worldtimeapi.org/api"
REQUEST_TIMEOUT_SECONDS = 10

# ------------------------------------------------------------
# Errors
# ------------------------------------------------------------

class WorldTimeServiceError(RuntimeError):
    pass

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _validate_timezone(timezone: str) -> None:
    if not timezone or "/" not in timezone:
        raise WorldTimeServiceError(
            "Invalid timezone format. Expected 'Area/Location'."
        )

# ------------------------------------------------------------
# Fetch & normalize
# ------------------------------------------------------------

def _fetch_time_data(timezone: str) -> Dict[str, Any]:
    url = f"{WORLD_TIME_API_BASE}/timezone/{timezone}"
    last_exc: Exception | None = None

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()

            try:
                return response.json()
            except ValueError as exc:
                raise WorldTimeServiceError(
                    "Invalid JSON response from WorldTimeAPI."
                ) from exc

        except requests.exceptions.Timeout as exc:
            last_exc = exc

        except requests.exceptions.HTTPError as exc:
            if response.status_code == 404:
                raise WorldTimeServiceError(
                    f"Unknown timezone '{timezone}'."
                ) from exc

            last_exc = exc

        except requests.exceptions.RequestException as exc:
            last_exc = exc

    raise WorldTimeServiceError(
        "WorldTimeAPI unavailable after retries."
    ) from last_exc


# ------------------------------------------------------------
# Public domain API
# ------------------------------------------------------------

def get_current_time_by_timezone(timezone: str) -> Dict[str, Any]:
    """
    Return current local time and timezone metadata for a given timezone.
    inputs:
        timezone: Timezone string in 'Area/Location' format, e.g., 'Europe/London'
    outputs:
        A dictionary containing current time and timezone information.
    """

    _validate_timezone(timezone)
    return _fetch_time_data(timezone)