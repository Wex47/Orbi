# # app/config/settings.py

# import os
# from typing import Optional
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     # --------------------
#     # App
#     # --------------------
#     APP_NAME: str = "Orbi"
#     ENV: str = "dev"

#     # --------------------
#     # Model
#     # --------------------
#     MODEL_NAME: str = "claude-sonnet-4-5-20250929"
#     MODEL_TEMP: float = 0.2

#     # MODEL KEYS
#     OPENAI_API_KEY: Optional[str]
#     GOOGLE_API_KEY: Optional[str]
#     ANTHROPIC_API_KEY: Optional[str]

#     # 
#     # Explicit env injection for testing purposes (intentional)
#     if self.anthropic_api_key:
#         os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key

#     if settings.openai_api_key:
#         os.environ["OPENAI_API_KEY"] = settings.openai_api_key

#     if settings.google_api_key:
#         os.environ["GOOGLE_API_KEY"] = settings.google_api_key

#     # --------------------
#     # Amadeus
#     # --------------------
#     AMADEUS_API_KEY: str
#     AMADEUS_API_SECRET: str
#     AMADEUS_BASE_URL: str = "https://test.api.amadeus.com"
#     AMADEUS_TOKEN_URL: str = "https://test.api.amadeus.com/v1/security/oauth2/token"

#     # --------------------
#     # Weather
#     # --------------------
#     OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com"

#     # --------------------
#     # HTTP
#     # --------------------
#     HTTP_TIMEOUT: int = 10

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#     )

# settings = Settings()

# app/config/settings.py

# import os
# from typing import Optional, Dict, Tuple
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from langchain.chat_models import init_chat_model

# from dotenv import load_dotenv
# load_dotenv()  # <-- must be before BaseSettings is instantiated

# class Settings(BaseSettings):
#     # --------------------
#     # App
#     # --------------------
#     APP_NAME: str = "Orbi"
#     ENV: str = "dev"

#     # --------------------
#     # Lightweight Model
#     # --------------------
#     LIGHTWEIGHT_MODEL_NAME: str = "claude-haiku-4-5-20251001"

#     # --------------------
#     # Model
#     # --------------------
#     MODEL_NAME: str = "claude-sonnet-4-5-20250929"
#     MODEL_TEMP: float = 0.2



#     # --------------------
#     # Verifier Model (Gemini)
#     # --------------------
#     VERIFIER_MODEL_NAME: str = "gemini-2.5-flash"
#     VERIFIER_TEMP: float = 0.0

#     # Model API keys
#     OPENAI_API_KEY: Optional[str] = None
#     GOOGLE_API_KEY: Optional[str] = None
#     ANTHROPIC_API_KEY: Optional[str] = None

#     # --------------------
#     # Amadeus
#     # --------------------
#     AMADEUS_API_KEY: str
#     AMADEUS_API_SECRET: str
#     AMADEUS_BASE_URL: str = "https://test.api.amadeus.com"
#     AMADEUS_TOKEN_URL: str = "https://test.api.amadeus.com/v1/security/oauth2/token"

#     # --------------------
#     # Weather
#     # --------------------
#     OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com"

#     # --------------------
#     # HTTP
#     # --------------------
#     HTTP_TIMEOUT: int = 10


#     # ------------------------------------------------------------------
#     # Pydantic config
#     # ------------------------------------------------------------------

#     # ------------------------------------------------------------------
#     # INTERNAL MODEL CACHE (class-level)
#     # ------------------------------------------------------------------
#     _model_cache: Dict[Tuple[str, float], object] = {}

#     # ------------------------------------------------------------------
#     # Public API
#     # ------------------------------------------------------------------
#     def get_chat_model(
#         self,
#         *,
#         temperature: Optional[float] = None,
#     ):
#         """
#         Return a cached LangChain chat model.

#         Models are cached per (MODEL_NAME, temperature).
#         """
#         temp = self.MODEL_TEMP if temperature is None else temperature
#         key = (self.MODEL_NAME, temp)

#         if key not in self._model_cache:
#             self._model_cache[key] = init_chat_model(
#                 self.MODEL_NAME,
#                 temperature=temp,
#             )

#         return self._model_cache[key]



# # --------------------
# # Instantiate settings
# # --------------------
# settings = Settings()

# # --------------------
# # Explicit env injection (intentional, centralized)
# # --------------------
# if settings.ANTHROPIC_API_KEY:
#     os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY

# if settings.OPENAI_API_KEY:
#     os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# if settings.GOOGLE_API_KEY:
#     os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY



# app/config/settings.py

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()  # must be before BaseSettings is instantiated


class Settings(BaseSettings):
    # --------------------
    # App
    # --------------------
    APP_NAME: str = "Orbi"
    ENV: str = "dev"

    # --------------------
    # Models
    # --------------------
    MODEL_NAME: str = "claude-sonnet-4-5-20250929"
    MODEL_TEMP: float = 0.2

    LIGHTWEIGHT_MODEL_NAME: str = "claude-haiku-4-5-20251001"
    LIGHTWEIGHT_MODEL_TEMP: float = 0.2

    VERIFIER_MODEL_NAME: str = "gemini-2.5-flash"
    VERIFIER_TEMP: float = 0.0

    # --------------------
    # API Keys
    # --------------------
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # --------------------
    # Amadeus
    # --------------------
    AMADEUS_API_KEY: str
    AMADEUS_API_SECRET: str
    AMADEUS_BASE_URL: str = "https://test.api.amadeus.com"
    AMADEUS_TOKEN_URL: str = "https://test.api.amadeus.com/v1/security/oauth2/token"

    # --------------------
    # Weather
    # --------------------
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com"

    # --------------------
    # HTTP
    # --------------------
    HTTP_TIMEOUT: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# --------------------
# Instantiate settings
# --------------------
settings = Settings()

# --------------------
# Explicit env injection (intentional & centralized)
# --------------------
if settings.ANTHROPIC_API_KEY:
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY

if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

if settings.GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
