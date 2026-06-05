from pydantic import BaseModel
from typing import Optional


class CodeChunk(BaseModel):
    chunk_id: str

    file_path: str

    language: str

    chunk_type: str

    symbol_name: Optional[str] = None

    start_line: int
    end_line: int

    content: str
