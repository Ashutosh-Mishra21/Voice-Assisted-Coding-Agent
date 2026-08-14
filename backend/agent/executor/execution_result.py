from dataclasses import dataclass, field
from typing import Any

from backend.agent.executor.execution_context import (
    ExecutionContext,
)

from backend.agent.planner.planner_step import (
    PlannerStep,
)


@dataclass
class ExecutionResult:
    """
    Represents the result of executing an ExecutionPlan.

    The ExecutionContext is retained so that the caller can access
    all intermediate and final execution artifacts.

    A successful execution contains:

        success=True
        executed_steps=[...]
        failed_step=None
        error=None
        context=<ExecutionContext>

    A failed execution contains:

        success=False
        executed_steps=[steps completed before failure]
        failed_step=<step that failed>
        error=<original exception>
        context=<ExecutionContext>
    """

    success: bool

    context: ExecutionContext

    executed_steps: list[PlannerStep] = field(
        default_factory=list,
    )

    failed_step: PlannerStep | None = None

    error: Exception | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def generation(self) -> Any | None:
        """
        Convenience accessor for the final generation result.
        """

        return self.context.generation

    @property
    def context_result(self) -> Any | None:
        """
        Convenience accessor for the generated context.
        """

        return self.context.context

    @property
    def prompt_result(self) -> Any | None:
        """
        Convenience accessor for the generated prompt.
        """

        return self.context.prompt

    @property
    def retrieved_results(self) -> Any | None:
        """
        Convenience accessor for retrieval results.
        """

        return self.context.retrieval_results

    @property
    def reranked_results(self) -> Any | None:
        """
        Convenience accessor for reranked results.
        """

        return self.context.reranked_results

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add metadata to the execution result.
        """

        self.metadata[key] = value
