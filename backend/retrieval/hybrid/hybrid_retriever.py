from backend.retrieval.semantic.semantic_retriever import SemanticRetriever

from backend.retrieval.bm25.bm25_retriever import BM25Retriever

from backend.retrieval.hybrid.fusion import ReciprocalRankFusion


class HybridRetriever:

    def __init__(
        self,
        repo_name: str,
    ):

        self.semantic = SemanticRetriever()

        self.bm25 = BM25Retriever(repo_name)

        self.fusion = ReciprocalRankFusion()

    def search(
        self,
        query: str,
        top_k: int = 10,
    ):

        semantic_results = self.semantic.search(
            query,
            top_k=top_k,
        )

        bm25_results = self.bm25.search(
            query,
            top_k=top_k,
        )

        ranked, documents = self.fusion.fuse(
            semantic_results,
            bm25_results,
        )

        final_results = []

        for chunk_id, _ in ranked:

            final_results.append(documents[chunk_id])

        return final_results[:top_k]
