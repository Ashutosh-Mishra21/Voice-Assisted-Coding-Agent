from pydantic import BaseModel


class AgentResponse(BaseModel):
    """
    Final response returned by the agent pipeline.
    """

    answer: str

    retrieved_chunks: int

    context_size: int

    prompt_size: int

    model_name: str
