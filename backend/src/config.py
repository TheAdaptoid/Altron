from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "AI Chat Backend"
    DEBUG: bool = False
    INFERENCE_URL: str = "http://localhost:8000/inference"

    class Config:
        """Pydantic configuration for environment variables."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
