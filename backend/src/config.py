from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: str
    REDIS_PASSWORD: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore"
    )

Config = Settings()
