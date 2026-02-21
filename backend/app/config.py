from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mobile_open_clo"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"
    OPENAI_WHISPER_MODEL: str = "whisper-1"
    TTS_MODEL: str = "tts-1"
    TTS_VOICE: str = "nova"

    model_config = {"env_file": ".env"}


settings = Settings()
