from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.

    Values are automatically loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APP_NAME: str = "KnowledgeOS"
    DEBUG: bool = False
    SECRET_KEY: str

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_URL: str

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    EMBEDDING_MODEL: str = "bge-m3"
    EMBEDDING_DIMENSION: int = 1024

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    OLLAMA_BASE_URL: str = "http://localhost:11434"



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()