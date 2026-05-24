import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CognitionOS"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PORT: int = 8000

    # JWT Authentication settings
    JWT_SECRET_KEY: str = "placeholder_key_must_be_overridden_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ENCRYPTION_KEY: str = "placeholder_32_byte_encryption_key_value"

    # Databases configurations
    DATABASE_URL: str = "postgresql+asyncpg://cognition_admin:cognition_secure_pass@localhost:5432/cognition_db"
    REDIS_URL: str = "redis://:redis_secure_pass@localhost:6379/0"
    
    # Vector DB settings
    VECTOR_DB_PROVIDER: str = "chroma"
    CHROMA_PERSIST_DIRECTORY: str = "./infrastructure/chroma_db"
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None

    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_TOKEN: Optional[str] = None

    # Ethical Governance settings
    ANONYMIZE_PII_IN_MEMORY: bool = True
    BIAS_MONITORING_THRESHOLD: float = 0.15
    ENABLE_EXPLAINABILITY_GENERATION: bool = True
    ALLOW_CLINICAL_ADVICE_EXTRACTION: bool = False

    # Observability
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
