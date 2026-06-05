from backend.codebase.indexer.repository_scanner import (
    RepositoryScanner,
)

from backend.codebase.indexer.chunk_builder import (
    ChunkBuilder,
)

from backend.codebase.parser.parser_factory import (
    ParserFactory,
)

from backend.codebase.parser.symbol_extractor import (
    SymbolExtractor,
)


class RepositoryIndexer:

    def __init__(self):

        self.scanner = RepositoryScanner()

        self.extractor = SymbolExtractor()

        self.chunk_builder = ChunkBuilder()

    def index_repository(
        self,
        repository_path: str,
    ):

        files = self.scanner.scan(repository_path)

        all_chunks = []

        total_functions = 0
        total_classes = 0

        for file in files:

            parser = ParserFactory.get_parser(str(file))

            tree, content = parser.parse_file(str(file))

            symbols = self.extractor.extract(tree.root_node)

            total_functions += sum(1 for s in symbols if s["type"] == "function")

            total_classes += sum(1 for s in symbols if s["type"] == "class")

            chunks = self.chunk_builder.build_chunks(
                file_path=str(file),
                content=content,
                symbols=symbols,
            )

            all_chunks.extend(chunks)

        return {
            "files": len(files),
            "functions": total_functions,
            "classes": total_classes,
            "chunks": all_chunks,
        }
