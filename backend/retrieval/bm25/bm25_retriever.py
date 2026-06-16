import numpy as np

from backend.retrieval.bm25.bm25_store import BM25Store
from backend.models.retrieval_result import RetrievalResult


class BM25Retriever:

    def __init__(
        self,
        repo_name: str,
    ):

        store = BM25Store()

        data = store.load(repo_name)

        self.bm25 = data["index"]

        self.chunks = data["chunks"]

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        top_indices = np.argsort(scores)[::-1]

        results = []

        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            chunk = self.chunks[idx]
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    score=float(scores[idx]),
                    file_path=chunk.file_path,
                    symbol_name=chunk.symbol_name,
                    content=chunk.content,
                    source="bm25",
                )
            )

            if len(results) >= top_k:
                break

        return results
