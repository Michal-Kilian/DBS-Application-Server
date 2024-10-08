from pydantic import BaseSettings
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("DATABASE_USER")
    POSTGRES_PASSWORD = os.getenv("DATABASE_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("DATABASE_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("DATABASE_PORT", 5432)
    POSTGRES_DB: str = os.getenv("DATABASE_NAME", "dbs")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    class Config:
        case_sensitive = True


settings = Settings()
