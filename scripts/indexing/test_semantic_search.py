from backend.codebase.indexer.repository_indexer import RepositoryIndexer

from backend.retrieval.semantic.index_pipeline import SemanticIndexPipeline

from backend.retrieval.semantic.semantic_retriever import SemanticRetriever

repo = "playground/sample_repo"

indexer = RepositoryIndexer()

result = indexer.index_repository(repo)

chunks = result["chunks"]

pipeline = SemanticIndexPipeline()

pipeline.index_chunks(chunks)

retriever = SemanticRetriever()

results = retriever.search("authentication logic")

print()
for r in results:

    print("=" * 50)

    print(r.symbol_name)

    print(r.file_path)

    print(round(r.score, 4))
