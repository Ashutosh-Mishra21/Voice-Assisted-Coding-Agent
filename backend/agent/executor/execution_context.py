from dataclasses import dataclass, field
from typing import Any

from backend.agent.agent_request import (
    AgentRequest,
)

from backend.agent.planner.execution_plan import (
    ExecutionPlan,
)


@dataclass
class ExecutionContext:
    """
    Runtime state shared between execution steps.

    An ExecutionContext belongs to exactly one execution of an
    AgentRequest against an ExecutionPlan.

    Steps read their required inputs from this object and store
    their outputs back into it.

    Example flow:

        RETRIEVE
            -> retrieval_results

        RERANK
            -> reranked_results

        BUILD_CONTEXT
            -> context

        BUILD_PROMPT
            -> prompt

        GENERATE
            -> generation
    """

    request: AgentRequest

    plan: ExecutionPlan

    conversation_history: str = ""

    retrieval_results: Any | None = None

    reranked_results: Any | None = None

    context: Any | None = None

    prompt: Any | None = None

    generation: Any | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store execution metadata.

        Metadata is intentionally unstructured so future execution
        steps can attach information without changing the context
        model every time a new capability is introduced.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve execution metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    def has_retrieval_results(self) -> bool:
        """
        Return True when retrieval has already been executed.
        """

        return self.retrieval_results is not None

    def has_reranked_results(self) -> bool:
        """
        Return True when reranking has already been executed.
        """

        return self.reranked_results is not None

    def has_context(self) -> bool:
        """
        Return True when context building has been executed.
        """

        return self.context is not None

    def has_prompt(self) -> bool:
        """
        Return True when prompt building has been executed.
        """

        return self.prompt is not None

    def has_generation(self) -> bool:
        """
        Return True when generation has been executed.
        """

        return self.generation is not None
