import pytest

from app.domain.climate.geo import geocode_place
from app.domain.climate.climate import get_monthly_climate_by_coords
from app.tools.tools import get_place_climate


# =========================================================
# DOMAIN FUNCTION TESTS – GEO
# =========================================================

def test_geocode_place_valid():
    result = geocode_place("Paris")

    print("\n[geocode_place valid]", result)

    assert isinstance(result, dict)
    assert "latitude" in result
    assert "longitude" in result
    assert result["name"].lower() == "paris"


def test_geocode_place_invalid():
    with pytest.raises(ValueError) as exc:
        geocode_place("Atlantis")

    print("\n[geocode_place invalid]", exc.value)

    assert "no coordinates found" in str(exc.value).lower()


# =========================================================
# DOMAIN FUNCTION TESTS – CLIMATE
# =========================================================

def test_get_monthly_climate_by_coords_valid():
    result = get_monthly_climate_by_coords(
        latitude=48.85,
        longitude=2.35,
        month="may"
    )

    print("\n[get_monthly_climate_by_coords valid]", result)

    assert isinstance(result, dict)
    assert "average_temperature_c" in result
    assert "average_precipitation_mm" in result


def test_get_monthly_climate_by_coords_invalid_month():
    with pytest.raises(ValueError) as exc:
        get_monthly_climate_by_coords(
            latitude=48.85,
            longitude=2.35,
            month="smarch"
        )

    print("\n[get_monthly_climate_by_coords invalid]", exc.value)

    assert "invalid month" in str(exc.value).lower()


# =========================================================
# TOOL TESTS – ORCHESTRATION
# =========================================================

def test_get_place_climate_valid():
    result = get_place_climate.invoke({
        "place_name": "Tokyo",
        "month": "October"
    })

    print("\n[get_place_climate valid]\n", result)

    assert isinstance(result, str)
    assert "tokyo" in result.lower()
    assert "avg temperature" in result.lower()


def test_get_place_climate_invalid():
    result = get_place_climate.invoke({
        "place_name": "Narnia",
        "month": "January"
    })

    print("\n[get_place_climate invalid]\n", result)

    assert isinstance(result, str)
    assert "no coordinates found" in result.lower()
