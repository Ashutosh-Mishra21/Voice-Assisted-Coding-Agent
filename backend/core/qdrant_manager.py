from qdrant_client import QdrantClient

from backend.config.paths import STORAGE_DIR

_client = None


def get_qdrant():

    global _client

    if _client is None:

        _client = QdrantClient(path=str(STORAGE_DIR / "qdrant"))

    return _client
