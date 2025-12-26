# app/infrastructure/llm.py

# from typing import Dict, Tuple, Optional
# from langchain.chat_models import init_chat_model
# from app.config.settings import settings
# import os

# _CHAT_MODEL_CACHE: Dict[Tuple[str, float, bool], object] = {}
# _LIGHTWEIGHT_CHAT_MODEL_CACHE: Dict[Tuple[str, float, bool], object] = {}
# _VERIFIER_MODEL: Optional[object] = None


# def get_chat_model(*, streaming: bool = False, temperature: Optional[float] = None):
#     temp = settings.MODEL_TEMP if temperature is None else temperature
#     key = (settings.MODEL_NAME, temp, streaming)

#     if key not in _CHAT_MODEL_CACHE:
#         _CHAT_MODEL_CACHE[key] = init_chat_model(
#             settings.MODEL_NAME,
#             temperature=temp,
#             streaming=streaming,
#         )

#     return _CHAT_MODEL_CACHE[key]


# def get_lightweight_chat_model(*, streaming: bool = False, temperature: Optional[float] = None):
#     temp = settings.MODEL_TEMP if temperature is None else temperature
#     key = (settings.MODEL_NAME, temp, streaming)

#     if key not in _LIGHTWEIGHT_CHAT_MODEL_CACHE:
#         _LIGHTWEIGHT_CHAT_MODEL_CACHE[key] = init_chat_model(
#             settings.LIGHTWEIGHT_MODEL_NAME,
#             temperature=temp,
#             streaming=streaming,
#         )

#     return _LIGHTWEIGHT_CHAT_MODEL_CACHE[key]



# def get_verifier_model():
#     global _VERIFIER_MODEL

#     if _VERIFIER_MODEL is None:
#         _VERIFIER_MODEL = init_chat_model(
#             settings.VERIFIER_MODEL_NAME,
#             model_provider="google_genai", # Force the use of the Google AI Studio / API Key path
#             api_key=settings.GOOGLE_API_KEY,
#             temperature=settings.VERIFIER_TEMP,
#             streaming=False,
#         )
    
#     return _VERIFIER_MODEL


# app/infrastructure/llm.py

from typing import Dict, Tuple, Optional
from langchain.chat_models import init_chat_model
from app.config.settings import settings

# ------------------------------------------------------------------
# Model caches
# ------------------------------------------------------------------

_CHAT_MODEL_CACHE: Dict[Tuple[str, float, bool], object] = {}
_LIGHTWEIGHT_MODEL_CACHE: Dict[Tuple[str, float, bool], object] = {}
_VERIFIER_MODEL: Optional[object] = None


# ------------------------------------------------------------------
# Main model (planner / executor / direct)
# ------------------------------------------------------------------

def get_chat_model(*, streaming: bool = False, temperature: Optional[float] = None):
    temp = settings.MODEL_TEMP if temperature is None else temperature
    key = (settings.MODEL_NAME, temp, streaming)

    if key not in _CHAT_MODEL_CACHE:
        _CHAT_MODEL_CACHE[key] = init_chat_model(
            settings.MODEL_NAME,
            temperature=temp,
            streaming=streaming,
        )

    return _CHAT_MODEL_CACHE[key]


# ------------------------------------------------------------------
# Lightweight model (router)
# ------------------------------------------------------------------

def get_lightweight_chat_model(
    *, streaming: bool = False, temperature: Optional[float] = None
):
    temp = (
        settings.LIGHTWEIGHT_MODEL_TEMP
        if temperature is None
        else temperature
    )
    key = (settings.LIGHTWEIGHT_MODEL_NAME, temp, streaming)

    if key not in _LIGHTWEIGHT_MODEL_CACHE:
        _LIGHTWEIGHT_MODEL_CACHE[key] = init_chat_model(
            settings.LIGHTWEIGHT_MODEL_NAME,
            temperature=temp,
            streaming=streaming,
        )

    return _LIGHTWEIGHT_MODEL_CACHE[key]


# ------------------------------------------------------------------
# Verifier model (deterministic, no streaming)
# ------------------------------------------------------------------

def get_verifier_model():
    global _VERIFIER_MODEL

    if _VERIFIER_MODEL is None:
        _VERIFIER_MODEL = init_chat_model(
            settings.VERIFIER_MODEL_NAME,
            model_provider="google_genai",
            api_key=settings.GOOGLE_API_KEY,
            temperature=settings.VERIFIER_TEMP,
            streaming=False,
        )

    return _VERIFIER_MODEL
