from typing import Any

from backend.agent.executor.execution_context import (
    ExecutionContext,
)

from backend.agent.executor.execution_result import (
    ExecutionResult,
)

from backend.agent.planner.planner_step import (
    PlannerStep,
    StepType,
)

from backend.generation.context.context_builder import (
    ContextBuilder,
)

from backend.generation.prompts.prompt_builder import (
    PromptBuilder,
)

from backend.monitoring import Metrics


class StepExecutor:
    """
    Executes individual PlannerStep instances.

    The StepExecutor owns the implementation details of execution
    steps, while AgentPipeline remains responsible for orchestration.

    Currently supported:

        RETRIEVE
        RERANK
        BUILD_CONTEXT
        BUILD_PROMPT
        GENERATE

    Future capabilities such as REVIEW, PATCH, and EXECUTE can be
    added here without turning AgentPipeline into a large collection
    of conditional branches.
    """

    def __init__(
        self,
        retriever: Any,
        reranker: Any,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        provider: Any,
    ):

        self.retriever = retriever

        self.reranker = reranker

        self.context_builder = context_builder

        self.prompt_builder = prompt_builder

        self.provider = provider

    def execute_step(
        self,
        step: PlannerStep,
        context: ExecutionContext,
    ) -> None:
        """
        Execute one planner step against the supplied execution
        context.

        The step modifies the ExecutionContext in place.

        Raises:
            NotImplementedError:
                If the planner produces a step type that this executor
                does not support yet.

            RuntimeError:
                If a step's required prerequisite is missing.
        """

        step_type = step.step_type

        if step_type == StepType.RETRIEVE:

            self._execute_retrieve(
                context=context,
            )

            return

        if step_type == StepType.RERANK:

            self._execute_rerank(
                context=context,
            )

            return

        if step_type == StepType.BUILD_CONTEXT:

            self._execute_build_context(
                context=context,
            )

            return

        if step_type == StepType.BUILD_PROMPT:

            self._execute_build_prompt(
                context=context,
            )

            return

        if step_type == StepType.GENERATE:

            self._execute_generate(
                context=context,
            )

            return

        raise NotImplementedError(
            f"Planner step '{step_type.value}' is not " f"implemented by StepExecutor."
        )

    def execute_plan(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Execute all steps in an ExecutionPlan in their declared order.

        PlannerStep.order determines execution order.

        Execution stops immediately when a step raises an exception.

        The original exception is retained inside ExecutionResult so
        AgentPipeline can re-raise it and preserve the existing
        application error behavior.
        """

        executed_steps: list[PlannerStep] = []

        ordered_steps = sorted(
            context.plan.steps,
            key=lambda step: step.order,
        )

        for step in ordered_steps:

            try:

                self.execute_step(
                    step=step,
                    context=context,
                )

                executed_steps.append(step)

            except Exception as exc:

                result = ExecutionResult(
                    success=False,
                    context=context,
                    executed_steps=executed_steps,
                    failed_step=step,
                    error=exc,
                )

                result.add_metadata(
                    "failed_step_order",
                    step.order,
                )

                result.add_metadata(
                    "failed_step_type",
                    step.step_type.value,
                )

                return result

        result = ExecutionResult(
            success=True,
            context=context,
            executed_steps=executed_steps,
        )

        result.add_metadata(
            "executed_step_count",
            len(executed_steps),
        )

        return result

    # ============================================================
    # RETRIEVE
    # ============================================================

    def _execute_retrieve(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Execute hybrid repository retrieval.
        """

        request = context.request

        with Metrics.retrieval_timer():

            retrieval_results = self.retriever.search(
                query=request.query,
                top_k=20,
            )

        context.retrieval_results = retrieval_results

        context.set_metadata(
            "retrieval_top_k",
            20,
        )

        context.set_metadata(
            "retrieval_result_count",
            len(retrieval_results),
        )

    # ============================================================
    # RERANK
    # ============================================================

    def _execute_rerank(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Execute cross-encoder reranking.

        Reranking requires retrieval to have completed first.
        """

        if context.retrieval_results is None:

            raise RuntimeError("RERANK step requires RETRIEVE step to execute first.")

        request = context.request

        with Metrics.rerank_timer():

            reranked = self.reranker.rerank(
                query=request.query,
                results=context.retrieval_results,
                top_k=request.top_k,
            )

        context.reranked_results = reranked

        context.set_metadata(
            "rerank_top_k",
            request.top_k,
        )

        context.set_metadata(
            "reranked_result_count",
            len(reranked),
        )

    # ============================================================
    # BUILD CONTEXT
    # ============================================================

    def _execute_build_context(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Build the LLM context from reranked repository results
        and conversation history.
        """

        if context.reranked_results is None:

            raise RuntimeError(
                "BUILD_CONTEXT step requires RERANK step " "to execute first."
            )

        request = context.request

        with Metrics.context_timer():

            built_context = self.context_builder.build(
                query=request.query,
                retrieved_chunks=context.reranked_results,
                conversation_history=context.conversation_history,
            )

        context.context = built_context

        Metrics.record_context_size(
            built_context.context_size,
        )

        Metrics.record_retrieved_chunks(
            built_context.num_chunks,
        )

        context.set_metadata(
            "context_size",
            built_context.context_size,
        )

        context.set_metadata(
            "context_num_chunks",
            built_context.num_chunks,
        )

    # ============================================================
    # BUILD PROMPT
    # ============================================================

    def _execute_build_prompt(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Build the LLM prompt from the generated context.
        """

        if context.context is None:

            raise RuntimeError(
                "BUILD_PROMPT step requires BUILD_CONTEXT step " "to execute first."
            )

        with Metrics.prompt_timer():

            prompt = self.prompt_builder.build(
                context=context.context,
            )

        context.prompt = prompt

        Metrics.record_prompt_size(
            prompt.prompt_size,
        )

        context.set_metadata(
            "prompt_size",
            prompt.prompt_size,
        )

    # ============================================================
    # GENERATE
    # ============================================================

    def _execute_generate(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Generate the final LLM response.
        """

        if context.prompt is None:

            raise RuntimeError(
                "GENERATE step requires BUILD_PROMPT step " "to execute first."
            )

        with Metrics.generation_timer(
            provider=self.provider.provider_name,
            model=self.provider.model,
        ):
            generation = self.provider.generate(
                context.prompt,
            )

        context.generation = generation

        context.set_metadata(
            "provider",
            self.provider.provider_name,
        )

        context.set_metadata(
            "model",
            self.provider.model,
        )

        context.set_metadata(
            "generation_model",
            generation.model_name,
        )
