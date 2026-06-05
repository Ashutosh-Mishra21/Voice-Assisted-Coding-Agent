from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
)

from backend.config.settings import settings

from backend.config.paths import STORAGE_DIR


class EmbeddingStore:

    def __init__(self):

        self.client = QdrantClient(path=str(STORAGE_DIR / "qdrant"))

    def create_collection(
        self,
        vector_size: int,
    ):

        collections = self.client.get_collections()

        existing = [c.name for c in collections.collections]

        if settings.QDRANT_COLLECTION not in existing:

            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
