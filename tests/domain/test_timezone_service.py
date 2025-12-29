import pytest

from app.domain.timezone_service import (
    get_current_time_by_timezone,
    WorldTimeServiceError,
)


def test_get_current_time_invalid_format_raises():
    """
    Invalid timezone format should be rejected locally,
    before any network call.
    """
    with pytest.raises(WorldTimeServiceError):
        get_current_time_by_timezone("UTC")  # missing "/"


def test_get_current_time_unknown_timezone_raises():
    """
    Valid format but unknown timezone is rejected by the API.
    """
    with pytest.raises(WorldTimeServiceError):
        get_current_time_by_timezone("Invalid/Timezone")


def test_get_current_time_valid_timezone_returns_dict():
    """
    Valid timezone returns current time data,
    assuming WorldTimeAPI is reachable.
    """
    result = get_current_time_by_timezone("Europe/London")

    assert isinstance(result, dict)
    assert "datetime" in result
    assert "timezone" in result