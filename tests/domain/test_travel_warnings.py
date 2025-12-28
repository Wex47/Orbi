from app.domain.travel_warnings import fetch_travel_warnings


def test_fetch_travel_warnings_known_country():
    result = fetch_travel_warnings("France")

    assert isinstance(result, set)


def test_fetch_travel_warnings_unknown_country():
    result = fetch_travel_warnings("Atlantis")

    assert result == set()
