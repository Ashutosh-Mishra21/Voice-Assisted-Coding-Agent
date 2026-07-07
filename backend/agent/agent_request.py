from pydantic import BaseModel


class AgentRequest(BaseModel):
    """
    Represents a single user request handled by the agent.
    """

    session_id: str

    repository_name: str

    query: str

    top_k: int = 5
