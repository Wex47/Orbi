# app/config/settings.py

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()  # must be before BaseSettings is instantiated


class Settings(BaseSettings):

    # --------------------
    # App
    # --------------------
    APP_NAME: str = "Orbi"
    ENV: str = "dev"

    # --------------------
    # 
    # --------------------
    
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
    CACHE_DIR: Path = PROJECT_ROOT / "app" / "cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


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

    #
    # RAPID API
    #
    RAPIDAPI_KEY: str

    # --------------------
    # HTTP
    # --------------------
    HTTP_TIMEOUT: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -----------------------
    # Database (Memory backup)
    # -----------------------

    postgres_host: str = Field(..., alias="POSTGRES_HOST")
    postgres_port: int = Field(..., alias="POSTGRES_PORT")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    @property
    def postgres_dsn(self) -> str:
        """
        Build a PostgreSQL DSN from structured settings.
        """
        return (
            f"postgresql://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
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