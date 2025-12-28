from typing import Optional
from app.infrastructure.amadeus_auth import AmadeusAuth
from app.infrastructure.amadeus_client_impl import AmadeusClient

_amadeus_client: Optional[AmadeusClient] = None

def get_amadeus_client() -> AmadeusClient:
    """
    Returns a singleton AmadeusClient instance.
    """
    global _amadeus_client

    if _amadeus_client is None:
        auth = AmadeusAuth()
        _amadeus_client = AmadeusClient(auth)

    return _amadeus_client
