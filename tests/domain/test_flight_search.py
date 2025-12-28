import pytest
from datetime import date, timedelta

from app.domain.flight_search import search_flights, FlightSearchError


def test_search_flights_happy_path():
    departure_date = date.today() + timedelta(days=1)

    result = search_flights(
        origin="TLV",
        destination="ATH",
        departure_date=departure_date,
        max_results=3,
    )

    assert isinstance(result, list)

    if result:
        offer = result[0]
        assert "id" in offer
        assert "total_price" in offer
        assert "currency" in offer
        assert "segments" in offer


def test_search_flights_invalid_origin_code_returns_empty_list():
    """
    Invalid IATA codes are treated as valid queries
    that simply return no results.
    """
    departure_date = date.today() + timedelta(days=1)

    result = search_flights(
        origin="INVALID",
        destination="DXB",
        departure_date=departure_date,
    )

    assert result == []


def test_search_flights_invalid_departure_date_raises_domain_error():
    """
    Invalid date type fails in the fetch layer
    and is wrapped as FlightSearchError.
    """
    with pytest.raises(FlightSearchError):
        search_flights(
            origin="TLV",
            destination="CDG",
            departure_date="not-a-date",  # type: ignore
        )
