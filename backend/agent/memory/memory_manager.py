from datetime import datetime

from backend.agent.memory.redis_store import RedisStore
from backend.agent.memory.memory_models import (
    ConversationMessage,
    ConversationHistory,
)


class MemoryManager:
    def __init__(self):
        self.store = RedisStore()

        if not self.store.ping():
            raise RuntimeError(
                "Redis is not running or is unreachable at localhost:6379. "
                "Start Redis before using MemoryManager."
            )

    def _session_key(
        self,
        session_id: str,
    ) -> str:
        return f"conversation:{session_id}"

    def get_history(
        self,
        session_id: str,
    ) -> ConversationHistory:
        data = self.store.load(self._session_key(session_id))

        if not data:
            return ConversationHistory(
                session_id=session_id,
                messages=[],
            )

        return ConversationHistory.model_validate(data)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        history = self.get_history(session_id)

        history.messages.append(
            ConversationMessage(
                role=role,
                content=content,
                timestamp=datetime.utcnow(),
            )
        )

        self.store.save(
            self._session_key(session_id),
            history.model_dump(mode="json"),
        )

    def clear_history(
        self,
        session_id: str,
    ) -> None:
        self.store.delete(self._session_key(session_id))

    def format_history(
        self,
        session_id: str,
        limit: int = 10,
    ) -> str:
        history = self.get_history(session_id)

        messages = history.messages[-limit:]

        parts = []

        for msg in messages:
            parts.append(f"{msg.role.upper()}: {msg.content}")

        return "\n".join(parts)
