from pydantic import BaseModel
from datetime import datetime
from typing import Any


class ConversationMessage(BaseModel):

    role: str

    content: str

    timestamp: datetime

    metadata: dict[str, Any] = {}


class ConversationHistory(BaseModel):

    session_id: str

    messages: list[ConversationMessage]
