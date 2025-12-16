from app.tools import geocode_place, get_monthly_climate


# def test_geocode_place_valid_city():
#     result = geocode_place.invoke({"place_name": "Tokyo"})
#     print(result)

#     # assert isinstance(result, str)
#     # assert "latitude" in result.lower()
#     # assert "longitude" in result.lower()


# def test_geocode_place_invalid_location():
#     result = geocode_place.invoke({"place_name": "ThisPlaceDoesNotExist123"})
#     print(result)
#     # assert isinstance(result, str)
#     # assert "no coordinates found" in result.lower() or "failed" in result.lower()


def test_get_monthly_climate_valid_input():
    result = get_monthly_climate.invoke({
        "latitude": 41.9028,
        "longitude": 12.4964,
        "month": 4
    })
    print(result)
    # assert isinstance(result, str)
    # assert "average temperature" in result.lower()


# def test_get_monthly_climate_invalid_month():
#     result = get_monthly_climate.invoke({
#         "latitude": 41.9028,
#         "longitude": 12.4964,
#         "month": 13
#     })
#     print(result)
#     # assert "month must be between" in result.lower()