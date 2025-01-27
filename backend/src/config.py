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
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    NEO4J_USER: str = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")
    NEO4J_URL: str = os.getenv("NEO4J_URL")


Config = Settings()
