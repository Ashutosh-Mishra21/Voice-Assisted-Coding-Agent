from pathlib import Path

from tree_sitter import Parser

from .base_parser import BaseParser


class TreeSitterParser(BaseParser):
    """Shared Tree-sitter file parsing implementation."""

    language_name: str

    def __init__(self, grammar):
        self.parser = Parser()
        self.parser.language = grammar()

    def parse_file(self, file_path: str):
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        tree = self.parser.parse(content.encode("utf-8"))
        return tree, content


class PythonParser(TreeSitterParser):
    language_name = "python"

    def __init__(self):
        from tree_sitter_python import language

        super().__init__(language)


class JavaParser(TreeSitterParser):
    language_name = "java"

    def __init__(self):
        from tree_sitter_java import language

        super().__init__(language)


class JavaScriptParser(TreeSitterParser):
    language_name = "javascript"

    def __init__(self):
        from tree_sitter_javascript import language

        super().__init__(language)


class TypeScriptParser(TreeSitterParser):
    language_name = "typescript"

    def __init__(self):
        from tree_sitter_typescript import language_typescript

        super().__init__(language_typescript)


class TSXParser(TreeSitterParser):
    language_name = "tsx"

    def __init__(self):
        from tree_sitter_typescript import language_tsx

        super().__init__(language_tsx)


class HTMLParser(TreeSitterParser):
    language_name = "html"

    def __init__(self):
        from tree_sitter_html import language

        super().__init__(language)


class CSSParser(TreeSitterParser):
    language_name = "css"

    def __init__(self):
        from tree_sitter_css import language

        super().__init__(language)


class MarkdownParser(BaseParser):
    """Read Markdown as an indexable document without code symbols."""

    language_name = "markdown"

    def parse_file(self, file_path: str):
        content = Path(file_path).read_text(encoding="utf-8")
        return None, content
