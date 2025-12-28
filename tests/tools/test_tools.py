from app.tools import tools


def test_get_place_climate_tool(monkeypatch):
    def fake_fetch_climate_data(place_name, month):
        return {
            "place": place_name,
            "month": month,
            "average_temperature_c": 20,
            "average_precipitation_mm": 50,
        }

    monkeypatch.setattr(
        tools,
        "fetch_climate_data",
        fake_fetch_climate_data,
    )

    result = tools.get_place_climate.invoke(
        {"place_name": "Paris", "month": "May"}
    )

    assert isinstance(result, dict)
    assert result["place"] == "Paris"
    assert result["month"] == "May"


def test_search_flights_tool(monkeypatch):
    def fake_search_flights(**kwargs):
        return [
            {
                "id": "1",
                "total_price": "100",
                "currency": "USD",
                "segments": [],
            }
        ]

    monkeypatch.setattr(
        tools,
        "search_flights",
        fake_search_flights,
    )

    result = tools.search_flights_tool.invoke(
        {
            "origin": "TLV",
            "destination": "CDG",
            "departure_date": "2025-01-01",
            "adults": 1,
            "max_results": 3,
        }
    )

    assert isinstance(result, list)
    assert result[0]["id"] == "1"


def test_travel_recommendations_tool(monkeypatch):
    def fake_get_travel_recommendations(city, country_code, k):
        return {
            "city": city,
            "recommendations": [{"name": "Museum"}],
        }

    monkeypatch.setattr(
        tools,
        "get_travel_recommendations",
        fake_get_travel_recommendations,
    )

    result = tools.travel_recommendations_tool.invoke(
        {"city": "Paris", "k": 1}
    )

    assert result["city"] == "Paris"
    assert len(result["recommendations"]) == 1


def test_get_current_time_tool(monkeypatch):
    def fake_get_current_time_by_timezone(timezone):
        return {
            "timezone": timezone,
            "datetime": "2025-01-01T12:00:00",
        }

    monkeypatch.setattr(
        tools,
        "get_current_time_by_timezone",
        fake_get_current_time_by_timezone,
    )

    result = tools.get_current_time.invoke(
        {"timezone": "Europe/London"}
    )

    assert result["timezone"] == "Europe/London"
    assert "datetime" in result


def test_get_current_local_datetime_tool():
    result = tools.get_current_local_datetime.invoke({})

    assert isinstance(result, str)
    assert len(result) >= 19  # YYYY-MM-DD HH:MM:SS


def test_get_travel_warnings_tool(monkeypatch):
    def fake_fetch_travel_warnings(country):
        return {"Warning A", "Warning B"}

    monkeypatch.setattr(
        tools,
        "fetch_travel_warnings",
        fake_fetch_travel_warnings,
    )

    result = tools.get_travel_warnings.invoke(
        {"country": "France"}
    )

    assert isinstance(result, list)
    assert sorted(result) == ["Warning A", "Warning B"]


def test_get_entry_requirements_tool(monkeypatch):
    def fake_get_visa_requirements(passport_country_code, destination_country_code):
        return {
            "passport": passport_country_code,
            "destination": destination_country_code,
            "visa": {},
        }

    monkeypatch.setattr(
        tools,
        "get_visa_requirements",
        fake_get_visa_requirements,
    )

    result = tools.get_entry_requirements.invoke(
        {"passport_country_code": "US", "destination_country_code": "FR"}
    )

    assert result["passport"] == "US"
    assert result["destination"] == "FR"


def test_get_israeli_embassy_contacts_tool(monkeypatch):
    def fake_get_israeli_embassies(country=None):
        return [{"country": country or "France", "phone": "123"}]

    monkeypatch.setattr(
        tools,
        "get_israeli_embassies",
        fake_get_israeli_embassies,
    )

    result = tools.get_israeli_embassy_contacts.invoke(
        {"country": "France"}
    )

    assert isinstance(result, list)
    assert result[0]["country"] == "France"
