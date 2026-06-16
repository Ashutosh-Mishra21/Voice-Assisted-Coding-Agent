from pydantic import BaseModel


class RetrievalResult(BaseModel):

    chunk_id: str

    score: float

    file_path: str

    symbol_name: str

    content: str

    source: str
