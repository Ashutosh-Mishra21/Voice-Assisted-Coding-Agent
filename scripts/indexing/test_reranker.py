from backend.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from backend.retrieval.rerank.reranker import (
    CrossEncoderReranker,
)

query = "authentication logic"

retriever = HybridRetriever("sample_repo")

results = retriever.search(
    query=query,
    top_k=20,
)

print("\nHYBRID RESULTS\n")

for i, result in enumerate(results, start=1):

    print(f"{i}. " f"{result.symbol_name} " f"({result.score:.4f})")

reranker = CrossEncoderReranker()

reranked = reranker.rerank(
    query=query,
    results=results,
    top_k=5,
)

print("\nRERANKED RESULTS\n")

for i, result in enumerate(
    reranked,
    start=1,
):

    print(
        f"{i}. "
        f"{result.symbol_name} "
        f"retrieval={result.retrieval_score:.4f} "
        f"rerank={result.rerank_score:.4f}"
    )
