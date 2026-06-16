from backend.config.settings import settings

from backend.retrieval.semantic.embedder import Embedder

from backend.retrieval.semantic.vector_store import VectorStore

from backend.models.retrieval_result import RetrievalResult


class SemanticRetriever:

    def __init__(self):

        self.embedder = Embedder()

        self.store = VectorStore()

    def search(self, query: str, top_k: int = 5):

        vector = self.embedder.embed_query(query)

        results = self.store.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=vector.tolist(),
            limit=top_k,
        )

        formatted = []

        for r in results.points:

            formatted.append(
                RetrievalResult(
                    chunk_id=r.payload["chunk_id"],
                    score=r.score,
                    file_path=r.payload["file_path"],
                    symbol_name=r.payload["symbol"],
                    content=r.payload["content"],
                    source="semantic",
                )
            )

        return formatted
