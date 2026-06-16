from backend.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from backend.retrieval.rerank.reranker import (
    CrossEncoderReranker,
)

from backend.generation.context.context_builder import (
    ContextBuilder,
)

from backend.generation.prompts.prompt_builder import (
    PromptBuilder,
)


def main():

    query = "authentication logic"

    print("\n" + "=" * 100)
    print("QUERY")
    print("=" * 100)
    print(query)

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    retriever = HybridRetriever("sample_repo")

    retrieval_results = retriever.search(
        query=query,
        top_k=20,
    )

    print("\n" + "=" * 100)
    print("HYBRID RETRIEVAL RESULTS")
    print("=" * 100)

    for idx, result in enumerate(
        retrieval_results,
        start=1,
    ):
        print(f"{idx}. " f"{result.symbol_name} " f"({result.score:.4f})")

    # --------------------------------------------------
    # Reranking
    # --------------------------------------------------

    reranker = CrossEncoderReranker()

    reranked_results = reranker.rerank(
        query=query,
        results=retrieval_results,
        top_k=5,
    )

    print("\n" + "=" * 100)
    print("RERANKED RESULTS")
    print("=" * 100)

    for idx, result in enumerate(
        reranked_results,
        start=1,
    ):
        print(
            f"{idx}. "
            f"{result.symbol_name} "
            f"retrieval={result.retrieval_score:.4f} "
            f"rerank={result.rerank_score:.4f}"
        )

    # --------------------------------------------------
    # Context Building
    # --------------------------------------------------

    context_builder = ContextBuilder()

    context_result = context_builder.build(
        query=query,
        retrieved_chunks=reranked_results,
        conversation_history=None,
    )

    print("\n" + "=" * 100)
    print("CONTEXT METADATA")
    print("=" * 100)

    print(f"Query        : {context_result.query}")
    print(f"Chunks Used  : {context_result.num_chunks}")
    print(f"Files Used   : {context_result.num_files}")
    print(f"Context Size : {context_result.context_size}")

    print("\n" + "=" * 100)
    print("GENERATED CONTEXT")
    print("=" * 100)

    print(context_result.context)

    # --------------------------------------------------
    # Prompt Building
    # --------------------------------------------------

    prompt_builder = PromptBuilder()

    prompt_result = prompt_builder.build(context=context_result)

    print("\n" + "=" * 100)
    print("PROMPT METADATA")
    print("=" * 100)

    print(f"Prompt Size : " f"{prompt_result.prompt_size}")

    print("\n" + "=" * 100)
    print("SYSTEM PROMPT")
    print("=" * 100)

    print(prompt_result.system_prompt)

    print("\n" + "=" * 100)
    print("USER PROMPT")
    print("=" * 100)

    print(prompt_result.user_prompt)

    print("\n" + "=" * 100)
    print("FULL PROMPT")
    print("=" * 100)

    print(prompt_result.full_prompt)


if __name__ == "__main__":
    main()
