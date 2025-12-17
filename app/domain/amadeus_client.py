import requests
from typing import Dict, Any
from app.domain.amadeus_auth import AmadeusAuth


class AmadeusClient:
    BASE_URL = "https://test.api.amadeus.com"

    def __init__(self, auth: AmadeusAuth):
        self.auth = auth

    def get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        token = self.auth.get_access_token()

        response = requests.get(
            f"{self.BASE_URL}{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        return response.json()
