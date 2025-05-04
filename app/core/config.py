# ✅ backend/app/core/config.py

from pydantic import BaseSettings
from sqlalchemy import create_engine


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "Beto9541!"
    db_name: str = "banco_meta"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

DATABASE_URL = (
    f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
