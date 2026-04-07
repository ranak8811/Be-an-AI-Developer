from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings managed via environment variables.
    Pydantic automatically matches these names with keys in the .env file.
    """
    # Database Configuration
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # LLM Configuration
    GEMINI_API_KEY: str

    # Chat Configuration
    MAX_HISTORY_MESSAGES: int = 2

    # App Settings
    APP_NAME: str = "AI Chatbot"

    # Database URL construction
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Load configuration from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings():
    """
    Returns a cached instance of the settings.
    lru_cache ensures we don't re-read the .env file every time we need a setting.
    """
    return Settings()

# Export an instance to be used across the app
settings = get_settings()
