from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    APP_NAME: str = "KrishiClinic AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/krishiclinic"

    AI_PROVIDER: str = "mock"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.1-flash-lite"
    GOOGLE_TRANSLATE_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen/qwen3.6-27b"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://frontend:3000",
        "http://127.0.0.1:3000",
        "https://frontend-woad-mu-58.vercel.app",
    ]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }

@lru_cache
def get_settings() -> Settings:
    return Settings()
