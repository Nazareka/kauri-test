from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    BINANCE_API_KEY: str
    BINANCE_API_SECRET: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        env_file_encoding = "utf-8"
        frozen = True

settings = Settings()

__all__ = ["settings"]