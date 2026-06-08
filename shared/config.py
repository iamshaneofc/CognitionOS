import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CognitionOS"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # JWT Authentication settings
    JWT_SECRET: str = "placeholder_key_must_be_overridden_in_production"
    JWT_ALGORITHM: str = "HS256"

    # Databases configurations
    DATABASE_URL: str = "postgresql+asyncpg://cognition_admin:cognition_secure_pass@localhost:5432/cognition_db"
    REDIS_URL: str = "redis://:redis_secure_pass@localhost:6379/0"
    
    # Vector DB & Models
    CHROMA_HOST: str = "localhost"
    PINECONE_API_KEY: Optional[str] = None
    MODEL_REGISTRY_PATH: str = "./infrastructure/models"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
