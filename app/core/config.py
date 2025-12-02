from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str

    database_url_sync: str
    database_url_async: str

    @property
    def database_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property
    def database_url_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    
settings = Settings()
