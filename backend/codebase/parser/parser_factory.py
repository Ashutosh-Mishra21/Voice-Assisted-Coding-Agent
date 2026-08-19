from pathlib import Path

from .parsers import (
    CSSParser,
    HTMLParser,
    JavaParser,
    JavaScriptParser,
    MarkdownParser,
    PythonParser,
    TSXParser,
    TypeScriptParser,
)


class ParserFactory:
    _PARSERS = {
        ".py": PythonParser,
        ".java": JavaParser,
        ".js": JavaScriptParser,
        ".jsx": JavaScriptParser,
        ".ts": TypeScriptParser,
        ".tsx": TSXParser,
        ".html": HTMLParser,
        ".css": CSSParser,
        ".scss": CSSParser,
        ".md": MarkdownParser,
    }

    @staticmethod
    def get_parser(file_path: str):
        suffix = Path(file_path).suffix.lower()
        parser_class = ParserFactory._PARSERS.get(suffix)

        if parser_class is None:
            raise ValueError(f"Unsupported file type: {suffix}")

        return parser_class()
