from pydantic import BaseModel


class ProviderResult(BaseModel):

    response: str

    model_name: str

    provider_name: str

    prompt_size: int

    completion_size: int

    total_size: int
