from pydantic_settings import BaseSettings, SettingsConfigDict

setting_config: SettingsConfigDict = SettingsConfigDict(
    arbitrary_types_allowed=True,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
)


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    APP_NAME: str = "AI Chat Backend"
    DEBUG: bool = False

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"


settings = Settings()
