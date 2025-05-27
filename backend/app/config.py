"""Application settings loaded from environment / .env file.

Auto‑generated documentation to improve code clarity.
"""


import os
from pathlib import Path
from pydantic import BaseSettings, AnyHttpUrl
from dotenv import load_dotenv

env_path = Path('.')/'.env'
if env_path.exists():
    load_dotenv(env_path)
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:euOkqpEVSgBhlWsPUMFSBTyXNauztgUJ@postgres.railway.internal:5432/railway")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

settings = Settings()

class CorsSettings(BaseSettings):
    origins: list[str] = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")]

cors_settings = CorsSettings()
