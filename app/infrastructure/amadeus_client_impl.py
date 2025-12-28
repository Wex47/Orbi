from typing import Dict, Any
import requests
from app.config.settings import settings
from app.infrastructure.amadeus_auth import AmadeusAuth

"""Client for interacting with the Amadeus API."""

class AmadeusClient:
    def __init__(self, auth: AmadeusAuth):
        self.auth = auth

    def get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        token = self.auth.get_access_token()

        try:
            response = requests.get(
                f"{settings.AMADEUS_BASE_URL}{path}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                params=params,
                timeout=settings.HTTP_TIMEOUT,
            )
        except requests.RequestException as e:
            return {
                "error": "Network error while calling Amadeus API",
                "details": str(e),
                "path": path,
                "params": params,
            }

        if not response.ok:
            return {
                "error": "Amadeus API error",
                "status_code": response.status_code,
                "details": response.text,
                "path": path,
                "params": params,
            }

        return response.json()