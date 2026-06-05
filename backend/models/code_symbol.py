from pydantic import BaseModel


class CodeSymbol(BaseModel):
    name: str
    symbol_type: str
    start_line: int
    end_line: int
