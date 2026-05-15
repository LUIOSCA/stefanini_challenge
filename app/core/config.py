from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_SSL: bool = True
    DB_ECHO: bool = False
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
