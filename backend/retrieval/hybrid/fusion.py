from collections import defaultdict

from backend.models.retrieval_result import RetrievalResult


class ReciprocalRankFusion:

    def fuse(
        self,
        semantic_results: list[RetrievalResult],
        bm25_results: list[RetrievalResult],
        k: int = 60,
    ):

        scores = defaultdict(float)

        documents = {}

        # Semantic Results
        for rank, result in enumerate(
            semantic_results,
            start=1,
        ):

            chunk_id = result.chunk_id

            scores[chunk_id] += 1 / (k + rank)

            documents[chunk_id] = result

        # BM25 Results
        for rank, result in enumerate(
            bm25_results,
            start=1,
        ):

            chunk_id = result.chunk_id

            scores[chunk_id] += 1 / (k + rank)

            # Prefer BM25 result if duplicate
            documents[chunk_id] = result

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked, documents
