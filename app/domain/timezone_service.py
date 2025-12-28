from typing import Dict, Any
import requests

WORLD_TIME_API_BASE = "http://worldtimeapi.org/api"

def get_current_time_by_timezone(timezone: str) -> Dict[str, Any]:
    """
    Fetch the current local time and timezone metadata for a given timezone.
    inputs: 
        timezone: Timezone string in the format 'Area/Location' (e.g., 'Europe/London')
    outputs:
        A dictionary with either:
            - On success:
                {
                    "status": "ok",
                    "data": { ... WorldTimeAPI response data ... }
                }
            - On error:
                {
                    "status": "error",
                    "error": "Error message describing the issue."
                }
    """
    
    if not timezone or "/" not in timezone:
        return {
            "status": "error",
            "error": "Invalid timezone format. Expected 'Area/Location'.",
        }

    url = f"{WORLD_TIME_API_BASE}/timezone/{timezone}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "WorldTimeAPI request timed out.",
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Network error while contacting WorldTimeAPI: {str(e)}",
        }

    if response.status_code == 404:
        return {
            "status": "error",
            "error": f"Unknown timezone '{timezone}'.",
        }

    if response.status_code != 200:
        return {
            "status": "error",
            "error": f"WorldTimeAPI error: HTTP {response.status_code}.",
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status": "error",
            "error": "Invalid JSON response from WorldTimeAPI.",
        }

    return {
        "status": "ok",
        "data": data,
    }