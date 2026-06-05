from pydantic import BaseModel


class SearchResult(BaseModel):
    score: float

    chunk_id: str

    file_path: str

    content: str
