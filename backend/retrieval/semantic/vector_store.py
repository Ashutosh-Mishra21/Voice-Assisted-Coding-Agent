from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams,
)
from backend.core.qdrant_manager import get_qdrant
from backend.config.settings import settings


class VectorStore:

    def __init__(self):

        self.client = get_qdrant()

    def create_collection(self, vector_size: int):

        collections = self.client.get_collections()

        names = [c.name for c in collections.collections]

        if settings.QDRANT_COLLECTION not in names:

            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert(self, points: list[PointStruct]):

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )
