from pathlib import Path

from tree_sitter import Language, Parser
from tree_sitter_python import language


class PythonParser:
    def __init__(self):

        self.parser = Parser()

        self.parser.language = Language(language())

    def parse_file(self, file_path: str):

        content = Path(file_path).read_text(encoding="utf-8")

        tree = self.parser.parse(content.encode("utf-8"))

        return tree, content
