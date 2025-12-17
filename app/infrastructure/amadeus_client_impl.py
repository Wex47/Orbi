import requests
from typing import Dict, Any
from app.infrastructure.amadeus_auth import AmadeusAuth
from app.config.settings import settings


class AmadeusClient:

    def __init__(self, auth: AmadeusAuth):
        self.auth = auth

    def get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        token = self.auth.get_access_token()

        response = requests.get(
            f"{settings.AMADEUS_BASE_URL}{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            params=params,
            timeout=settings.HTTP_TIMEOUT,
        )

        response.raise_for_status()
        return response.json()
