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

from backend.generation.providers.ollama_provider import (
    OllamaProvider,
)


def main():

    query = "Explain how authentication works " "in this repository."

    print("\n" + "=" * 100)
    print("USER QUERY")
    print("=" * 100)
    print(query)

    # ==================================================
    # RETRIEVAL
    # ==================================================

    retriever = HybridRetriever(repository_name="sample_repo")

    retrieval_results = retriever.search(
        query=query,
        top_k=20,
    )

    print("\n" + "=" * 100)
    print("HYBRID RESULTS")
    print("=" * 100)

    for index, result in enumerate(
        retrieval_results,
        start=1,
    ):
        print(f"{index}. " f"{result.symbol_name} " f"({result.score:.4f})")

    # ==================================================
    # RERANKING
    # ==================================================

    reranker = CrossEncoderReranker()

    reranked_results = reranker.rerank(
        query=query,
        results=retrieval_results,
        top_k=5,
    )

    print("\n" + "=" * 100)
    print("RERANKED RESULTS")
    print("=" * 100)

    for index, result in enumerate(
        reranked_results,
        start=1,
    ):
        print(
            f"{index}. "
            f"{result.symbol_name} "
            f"retrieval={result.retrieval_score:.4f} "
            f"rerank={result.rerank_score:.4f}"
        )

    # ==================================================
    # CONTEXT BUILDING
    # ==================================================

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

    # ==================================================
    # PROMPT BUILDING
    # ==================================================

    prompt_builder = PromptBuilder()

    prompt_result = prompt_builder.build(
        context=context_result,
    )

    print("\n" + "=" * 100)
    print("PROMPT METADATA")
    print("=" * 100)

    print(f"Prompt Size : " f"{prompt_result.prompt_size}")

    # ==================================================
    # GENERATION
    # ==================================================

    provider = OllamaProvider(model="qwen3:8b")

    generation_result = provider.generate(
        prompt=prompt_result,
    )

    print("\n" + "=" * 100)
    print("GENERATION METADATA")
    print("=" * 100)

    print(f"Model            : " f"{generation_result.model_name}")

    print(f"Prompt Size      : " f"{generation_result.prompt_size}")

    print(f"Completion Size  : " f"{generation_result.completion_size}")

    print(f"Total Size       : " f"{generation_result.total_size}")

    # ==================================================
    # FINAL ANSWER
    # ==================================================

    print("\n" + "=" * 100)
    print("MODEL RESPONSE")
    print("=" * 100)

    print(generation_result.response)


if __name__ == "__main__":
    main()
