from __future__ import annotations
from typing import Dict, Any, Optional
import requests
from app.config.settings import settings
import json


TRAVEL_BUDDY_URL = "https://visa-requirement.p.rapidapi.com/v2/visa/check"
TRAVEL_BUDDY_HOST = "visa-requirement.p.rapidapi.com"


class VisaServiceError(RuntimeError):
    pass


# ============================================================
# Public API (THIS is what the tool calls)
# ============================================================

def get_visa_requirements(
    passport_country_code: str,
    destination_country_code: str,
) -> Dict[str, Any]:
    """
    Central domain function for visa & entry requirements.

    Owns:
    - API integration
    - normalization of optional fields
    - interpretation of visa rules
    """

    raw = _fetch_raw(
        passport_country_code,
        destination_country_code,
    )

    data = raw.get("data") or {}
    visa_rules = data.get("visa_rules") or {}

    primary = _normalize_rule(visa_rules.get("primary_rule"))
    secondary = _normalize_rule(visa_rules.get("secondary_rule"))
    exception = _normalize_rule(visa_rules.get("exception_rule"))
    mandatory = _normalize_rule(data.get("mandatory_registration"))

    return {
        "passport": data.get("passport"),
        "destination": data.get("destination"),

        "visa": {
            "summary": _build_visa_summary(primary, secondary),
            "primary_rule": primary,
            "secondary_rule": secondary,
            "exception_rule": exception,
        },

        "mandatory_registration": mandatory,

        "source": "Travel Buddy (RapidAPI)",
        "disclaimer": "Visa rules may change. Always verify with official sources.",
    }


# ============================================================
# Internal helpers (private to this domain)
# ============================================================

def _fetch_raw(
    passport: str,
    destination: str,
) -> Dict[str, Any]:

    headers = {
        "User-Agent": "Orbi/1.0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": TRAVEL_BUDDY_HOST,
    }

    payload = {
        "passport": passport.upper(),
        "destination": destination.upper(),
    }

    try:
        response = requests.post(
            TRAVEL_BUDDY_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise VisaServiceError("Failed to fetch visa requirements") from exc


def _normalize_rule(
    rule: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Normalize rule-like objects:
    - mandatory_registration
    - primary / secondary visa rules
    - exception rule

    Missing or empty rules return None.
    """
    if not rule:
        return None

    return {
        "name": rule.get("name"),
        "duration": rule.get("duration"),
        "color": rule.get("color"),
        "link": rule.get("link"),
        "full_text": rule.get("full_text"),
        "exception_type": rule.get("exception_type_name"),
        "country_codes": rule.get("country_codes"),
    }


def _build_visa_summary(
    primary: Optional[Dict[str, Any]],
    secondary: Optional[Dict[str, Any]],
) -> str:
    """
    Build a concise, customer-facing visa rule line
    according to Travel Buddy rules.
    """

    if not primary and not secondary:
        return "Visa information unavailable"

    names = []
    if primary and primary.get("name"):
        names.append(primary["name"])
    if secondary and secondary.get("name"):
        names.append(secondary["name"])

    rule_part = " / ".join(names)

    duration = (
        (primary or {}).get("duration")
        or (secondary or {}).get("duration")
    )

    return f"{rule_part} – {duration}" if duration else rule_part