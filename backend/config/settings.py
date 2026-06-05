from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    APP_NAME: str = "Voice Assisted Coding Agent"

    APP_VERSION: str = "0.1.0"

    DEBUG: bool = True

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    RERANK_MODEL: str = "BAAI/bge-reranker-base"

    DEFAULT_TOP_K: int = 10

    QDRANT_COLLECTION: str = "repository_chunks"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
