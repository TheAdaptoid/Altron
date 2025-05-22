from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    APP_NAME: str = "AI Chat Backend"
    DEBUG: bool = False
    INFERENCE_URL: str = "http://localhost:8000/inference"

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"

    class Config:
        """Pydantic configuration for environment variables."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
