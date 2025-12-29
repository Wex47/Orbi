from __future__ import annotations
from typing import Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


# Load .env early, before Settings instantiation
load_dotenv()


class Settings(BaseSettings):
    # --------------------
    # App
    # --------------------
    APP_NAME: str = "Orbi"
    ENV: str = "dev"
    THREAD_ID: str = "123" # fixed for testing persistence. you can change to None to check non-persistence.

    # --------------------
    # Logging
    # --------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    LOG_FILE_NAME: str = "app.log"
    LOG_MAX_BYTES: int = 5_000_000  # 5 MB
    LOG_BACKUP_COUNT: int = 3
    SUCCESS_GENERIC: str = "invocation succeeded"
    FAILED_GENERIC: str = "invocation failed"

    # --------------------
    # Paths
    # --------------------
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
    DATA_DIR: Path = PROJECT_ROOT / "app" / "data"
    CACHE_DIR: Path = PROJECT_ROOT / "app" / "cache"

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
    # Summarization
    # --------------------
    MAX_SUMMARY_INPUT_TOKENS: int = 6000
    SUMMARY_TOKENS_THRESHOLD: int = 4000
    MAX_SUMMARY_OUTPUT_TOKENS: int = 256

    # --------------------
    # API Keys
    # --------------------
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # --------------------
    # Amadeus
    # --------------------
    AMADEUS_API_KEY: str
    AMADEUS_API_SECRET: str
    AMADEUS_BASE_URL: str = "https://test.api.amadeus.com"
    AMADEUS_TOKEN_URL: str = (
        "https://test.api.amadeus.com/v1/security/oauth2/token"
    )

    # --------------------
    # Weather
    # --------------------
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com"

    # --------------------
    # Government APIs
    # --------------------
    GOV_IL_API_URL: str = "https://data.gov.il/api/3/action/datastore_search"

    # --------------------
    # RapidAPI
    # --------------------
    RAPIDAPI_KEY: str

    # --------------------
    # HTTP
    # --------------------
    HTTP_TIMEOUT: int = 10

    # --------------------
    # Database
    # --------------------
    POSTGRES_HOST: str = Field(..., alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., alias="POSTGRES_PORT")
    POSTGRES_USER: str = Field(..., alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., alias="POSTGRES_DB")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Singleton settings object
settings = Settings()