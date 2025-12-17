import time
import requests
from typing import Optional
from app.config.settings import settings

class AmadeusAuth:

    def __init__(self):
        self.api_key = settings.AMADEUS_API_KEY
        self.api_secret = settings.AMADEUS_API_SECRET

        self._access_token: Optional[str] = None
        self._expires_at: float = 0.0

    def get_access_token(self) -> str:
        """
        Returns a valid access token.
        Fetches a new one if missing or expired.
        """
        if self._access_token and time.time() < self._expires_at:
            return self._access_token

        response = requests.post(
            settings.AMADEUS_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.api_secret,
            },
            timeout=10,
        )

        response.raise_for_status()
        payload = response.json()

        self._access_token = payload["access_token"]

        # subtract 60s as a safety buffer
        self._expires_at = time.time() + payload["expires_in"] - 60

        return self._access_token