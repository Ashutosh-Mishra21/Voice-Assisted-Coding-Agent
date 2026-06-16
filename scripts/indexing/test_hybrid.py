from backend.retrieval.hybrid.hybrid_retriever import HybridRetriever

retriever = HybridRetriever("sample_repo")

results = retriever.search("authentication login")

for result in results:

    print()
    print(result.chunk_id, result.symbol_name)
    print(result.symbol_name)

    print(result.source)

    print(result.score)
