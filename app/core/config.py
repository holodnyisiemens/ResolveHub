from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    database_url_sync: str
    database_url_async: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
