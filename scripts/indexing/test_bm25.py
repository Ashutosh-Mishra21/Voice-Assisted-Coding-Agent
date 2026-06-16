from backend.codebase.indexer.repository_indexer import RepositoryIndexer

from backend.retrieval.bm25.bm25_indexer import BM25Indexer

from backend.retrieval.bm25.bm25_store import BM25Store

from backend.retrieval.bm25.bm25_retriever import BM25Retriever

repo = "playground/sample_repo"

indexer = RepositoryIndexer()

result = indexer.index_repository(repo)

chunks = result["chunks"]

bm25 = BM25Indexer().build(chunks)

BM25Store().save(
    repo_name="sample_repo",
    bm25_index=bm25,
    chunks=chunks,
)

retriever = BM25Retriever("sample_repo")

results = retriever.search("login")

for result in results:

    print()

    print(result.symbol_name)

    print(result.score)
