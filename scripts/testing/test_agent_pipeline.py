from backend.agent.pipeline import AgentPipeline
from backend.agent.agent_request import AgentRequest
from backend.agent.memory.memory_manager import MemoryManager
from backend.core.model_registry import ModelRegistry

from backend.codebase.indexer.repository_indexer import RepositoryIndexer
from backend.retrieval.bm25.bm25_indexer import BM25Indexer
from backend.retrieval.bm25.bm25_store import BM25Store
from backend.retrieval.hybrid.hybrid_retriever import HybridRetriever


def main():
    repo_path = "playground/tourism-website-main"
    repo_name = "tourism-website-main"

    # --------------------------------------------------
    # 1) Index repository
    # --------------------------------------------------
    indexer = RepositoryIndexer()
    result = indexer.index_repository(repo_path)

    print(f"Indexed files: {result['files']}")
    print(f"Indexed functions: {result['functions']}")
    print(f"Indexed classes: {result['classes']}")
    print(f"Indexed chunks: {len(result['chunks'])}")

    # --------------------------------------------------
    # 2) Build BM25 index and save it
    # --------------------------------------------------
    chunks = result["chunks"]
    bm25 = BM25Indexer().build(chunks)

    BM25Store().save(
        repo_name=repo_name,
        bm25_index=bm25,
        chunks=chunks,
    )

    print(f"Saved BM25 index to storage/bm25/{repo_name}.pkl")

    # --------------------------------------------------
    # 3) Quick retrieval verification
    # --------------------------------------------------
    retriever = HybridRetriever(repo_name)
    retrieved = retriever.search("navigation bar", top_k=5)

    print("\nRetrieval preview:")
    for r in retrieved:
        print(f"- {r.symbol_name} | {r.source} | score={r.score:.4f}")

    # --------------------------------------------------
    # 4) Run agent pipeline
    # --------------------------------------------------
    registry = ModelRegistry()
    memory = MemoryManager()

    pipeline = AgentPipeline(
        repository_name=repo_name,
        registry=registry,
        memory=memory,
    )

    request = AgentRequest(
        session_id="session-002",
        repository_name=repo_name,
        query="Explain how navigation bar works in this codebase.",
    )

    response = pipeline.ask(request)

    print("\n" + "=" * 100)
    print("AGENT RESPONSE")
    print("=" * 100)
    print(f"Model             : {response.model_name}")
    print(f"Retrieved Chunks  : {response.retrieved_chunks}")
    print(f"Context Size      : {response.context_size}")
    print(f"Prompt Size       : {response.prompt_size}")

    print("\n" + "=" * 100)
    print("ANSWER")
    print("=" * 100)
    print(response.answer)

    print("\n" + "=" * 100)
    print("CONVERSATION HISTORY")
    print("=" * 100)
    print(memory.format_history(request.session_id))


if __name__ == "__main__":
    main()
