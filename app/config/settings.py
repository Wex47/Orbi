# app/config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --------------------
    # App
    # --------------------
    APP_NAME: str = "Orbi"
    ENV: str = "dev"

    # --------------------
    # Model
    # --------------------
    MODEL_NAME: str = "claude-sonnet-4-5-20250929"
    MODEL_TEMP: float = 0.2

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
    )

settings = Settings()