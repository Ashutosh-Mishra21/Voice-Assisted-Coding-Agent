from backend.codebase.indexer.repository_indexer import RepositoryIndexer


def main():

    repo = "playground/sample_repo"

    indexer = RepositoryIndexer()

    result = indexer.index_repository(repo)

    print()

    print(f"Files: {result['files']}")

    print(f"Functions: {result['functions']}")

    print(f"Classes: {result['classes']}")

    print(f"Chunks: {len(result['chunks'])}")

    print()

    for chunk in result["chunks"][:10]:

        print(f"{chunk.chunk_type} | " f"{chunk.symbol_name}")


if __name__ == "__main__":
    main()
