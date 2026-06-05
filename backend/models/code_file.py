from pydantic import BaseModel


class CodeFile(BaseModel):
    path: str

    language: str

    content: str
