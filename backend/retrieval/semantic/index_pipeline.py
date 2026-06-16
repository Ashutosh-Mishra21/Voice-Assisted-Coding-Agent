from qdrant_client.models import PointStruct

from backend.retrieval.semantic.embedder import Embedder

from backend.retrieval.semantic.vector_store import VectorStore
from backend.config.settings import settings

class SemanticIndexPipeline:

    def __init__(self):

        self.embedder = Embedder()

        self.store = VectorStore()

    def index_chunks(self, chunks):

        texts = [chunk.content for chunk in chunks]

        vectors = self.embedder.embed_texts(texts)

        vector_size = len(vectors[0])

        self.store.create_collection(vector_size)

        points = []

        for chunk, vector in zip(chunks, vectors):

            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=vector.tolist(),
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "file_path": chunk.file_path,
                        "symbol": chunk.symbol_name,
                        "content": chunk.content,
                    },
                )
            )
        print(f"Chunks: {len(chunks)}")
        print(f"Vectors: {len(vectors)}")
        print(f"Points: {len(points)}")
        operation = self.store.upsert(points)

        print(operation)
        info = self.store.client.get_collection(settings.QDRANT_COLLECTION)

        print(info.points_count)
        return len(points)
