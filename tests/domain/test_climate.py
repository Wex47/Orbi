import pytest
from app.domain.climate import fetch_climate_data


def test_fetch_climate_data_happy_path():
    result = fetch_climate_data("Paris", "may")

    assert result["place"]
    assert result["country"]
    assert result["month"] == "May"
    assert isinstance(result["average_temperature_c"], (int, float))
    assert isinstance(result["average_precipitation_mm"], (int, float))


def test_fetch_climate_data_month_as_int():
    result = fetch_climate_data("Berlin", 5)

    assert result["month"] == "May"


def test_fetch_climate_data_invalid_month_raises():
    with pytest.raises(ValueError, match="Invalid month"):
        fetch_climate_data("Rome", "not-a-month")