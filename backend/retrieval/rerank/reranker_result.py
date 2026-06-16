from pydantic import BaseModel


class RerankResult(BaseModel):
    chunk_id: str

    file_path: str
    symbol_name: str
    content: str

    retrieval_score: float
    rerank_score: float

    source: str
