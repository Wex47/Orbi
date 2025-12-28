import pytest
from app.domain.travel_recommendations import (
    get_travel_recommendations,
    TravelRecommendationError,
)

def test_get_travel_recommendations_happy_path():
    result = get_travel_recommendations("Paris", k=3)

    assert "city" in result
    assert "recommendations" in result
    assert len(result["recommendations"]) <= 3


def test_get_travel_recommendations_unknown_city_raises_domain_error():
    with pytest.raises(TravelRecommendationError):
        get_travel_recommendations("ThisCityDoesNotExist")


def test_get_travel_recommendations_k_zero_returns_empty_list():
    result = get_travel_recommendations("Paris", k=0)

    assert result["recommendations"] == []