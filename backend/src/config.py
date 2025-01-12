import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")


Config = Settings()
