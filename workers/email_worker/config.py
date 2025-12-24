from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            ".env.local",
        ],
        extra="ignore",
    )

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_PASSWORD: SecretStr
    IMAP_HOST: str
    IMAP_PORT: str
    IMAP_USER: EmailStr
    IMAP_PASSWORD: SecretStr
    EMAIL_FOR_TESTS: EmailStr
    API_URL: str


settings = Settings()
