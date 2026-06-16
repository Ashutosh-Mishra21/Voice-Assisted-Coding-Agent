from backend.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from backend.retrieval.rerank.reranker import (
    CrossEncoderReranker,
)

from backend.generation.context.context_builder import (
    ContextBuilder,
)


def main():

    query = "authentication logic"

    retriever = HybridRetriever("sample_repo")

    results = retriever.search(
        query=query,
        top_k=20,
    )

    reranker = CrossEncoderReranker()

    reranked = reranker.rerank(
        query=query,
        results=results,
        top_k=5,
    )

    builder = ContextBuilder()

    context = builder.build(
        query=query,
        retrieved_chunks=reranked,
        conversation_history=None,
    )

    print("\n")
    print("=" * 100)
    print("GENERATED CONTEXT")
    print("=" * 100)
    print(context)


if __name__ == "__main__":
    main()
