# import pytest
# from app.domain.entry_requirements import get_visa_requirements


# def test_get_visa_requirements_happy_path():
#     result = get_visa_requirements("US", "FR")

#     assert isinstance(result, dict)
#     assert "summary" in result.get("visa", {})
#     assert "mandatory_registration" in result


# def test_get_visa_requirements_invalid_passport_code():
#     with pytest.raises(ValueError):
#         get_visa_requirements("XXX", "FR")


# def test_get_visa_requirements_invalid_destination_code():
#     with pytest.raises(ValueError):
#         get_visa_requirements("US", "ZZ")

from app.domain.entry_requirements import get_visa_requirements


def test_get_visa_requirements_happy_path():
    result = get_visa_requirements("US", "FR")

    assert isinstance(result, dict)

    # Top-level invariants (always present)
    assert "passport" in result
    assert "destination" in result
    assert "visa" in result
    assert "mandatory_registration" in result
    assert "source" in result
    assert "disclaimer" in result

    # Visa block invariants
    visa = result["visa"]
    assert isinstance(visa, dict)
    assert "summary" in visa
    assert "primary_rule" in visa
    assert "secondary_rule" in visa
    assert "exception_rule" in visa


def test_get_visa_requirements_unknown_passport_code():
    result = get_visa_requirements("XX", "FR")

    # Should not crash
    assert isinstance(result, dict)

    # Structure still guaranteed
    assert "visa" in result
    assert "mandatory_registration" in result

    # Passport may be None or missing
    assert result["passport"] is None or isinstance(result["passport"], dict)


def test_get_visa_requirements_unknown_destination_code():
    result = get_visa_requirements("US", "ZZ")

    # Graceful degradation
    assert isinstance(result, dict)

    assert "destination" in result
    assert result["destination"] is None or isinstance(result["destination"], dict)


def test_get_visa_requirements_both_codes_unknown():
    result = get_visa_requirements("XX", "YY")

    assert isinstance(result, dict)

    # Still returns normalized structure
    assert "visa" in result
    assert isinstance(result["visa"], dict)
