from pathlib import Path

from pydantic import BaseModel, EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    employees: str = "/employees"
    tasks: str = "/tasks"
    auth: str = "/auth"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10
    token_type: str = "Bearer"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            ".env.local",
        ],
        extra="ignore",
    )

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str
    JWT_SECRET_KEY: str

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

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()

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

    @property
    def token_url(self) -> str:
        return f"{self.api.prefix}" f"{self.api.v1.prefix}" f"{self.api.v1.auth}/login"


settings = Settings()
