from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Meeting Notes to Professional Email Assistant"
    environment: str = "development"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    database_url: str = "postgresql+psycopg://meeting:meeting@db:5432/meeting_email"
    max_transcript_chars: int = 30_000
    llm_timeout_seconds: int = 30
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
