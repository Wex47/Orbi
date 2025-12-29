import pytest
from app.infrastructure import amadeus_client


@pytest.fixture(autouse=True)
def reset_amadeus_client():
    """
    Reset the global singleton between tests.
    """
    amadeus_client._amadeus_client = None


def test_get_amadeus_client_singleton(monkeypatch):
    created_clients = []

    class FakeAuth:
        pass

    class FakeClient:
        def __init__(self, auth):
            self.auth = auth
            created_clients.append(self)

    monkeypatch.setattr(amadeus_client, "AmadeusAuth", FakeAuth)
    monkeypatch.setattr(amadeus_client, "AmadeusClient", FakeClient)

    c1 = amadeus_client.get_amadeus_client()
    c2 = amadeus_client.get_amadeus_client()

    assert c1 is c2
    assert len(created_clients) == 1
    assert isinstance(c1.auth, FakeAuth)