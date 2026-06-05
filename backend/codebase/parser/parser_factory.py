from pathlib import Path

from .python_parser import PythonParser


class ParserFactory:

    @staticmethod
    def get_parser(file_path: str):

        suffix = Path(file_path).suffix

        if suffix == ".py":
            return PythonParser()

        raise ValueError(f"Unsupported file type: {suffix}")
