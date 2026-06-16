from pydantic import BaseModel


class PromptResult(BaseModel):

    system_prompt: str

    user_prompt: str

    full_prompt: str

    prompt_size: int
