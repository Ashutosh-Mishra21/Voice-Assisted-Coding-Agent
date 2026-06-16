from pydantic import BaseModel


class ContextResult(BaseModel):

    context: str

    query: str

    num_chunks: int

    num_files: int

    context_size: int
