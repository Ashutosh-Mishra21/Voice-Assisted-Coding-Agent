from backend.agent.agent_request import (
    AgentRequest,
)

from backend.agent.agent_response import (
    AgentResponse,
)
from backend.agent.executor import (
    ExecutionContext,
    ExecutionResult,
    StepExecutor,
)

from backend.agent.memory.memory_manager import (
    MemoryManager,
)

from backend.agent.planner.execution_plan import (
    ExecutionPlan,
)

from backend.agent.planner.planner import (
    Planner,
)

from backend.core.model_registry import (
    ModelRegistry,
)

from backend.generation.context.context_builder import (
    ContextBuilder,
)

from backend.generation.prompts.prompt_builder import (
    PromptBuilder,
)

from backend.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from backend.monitoring import (
    Metrics,
)


class AgentPipeline:
    """
    Main orchestration layer for agent execution.

    AgentPipeline is responsible for:

        1. Receiving an AgentRequest
        2. Obtaining an ExecutionPlan from Planner
        3. Reading conversation memory
        4. Creating an ExecutionContext
        5. Executing the plan through StepExecutor
        6. Updating conversation memory
        7. Converting ExecutionResult into AgentResponse

    AgentPipeline does not implement individual execution steps.

    Individual steps are implemented by StepExecutor.
    """

    def __init__(
        self,
        repository_name: str,
        registry: ModelRegistry,
        memory: MemoryManager,
        planner: Planner | None = None,
    ):

        self.repository_name = repository_name

        self.memory = memory

        self.registry = registry

        self.planner = planner or Planner()

        # ========================================================
        # Existing repository/retrieval components
        # ========================================================

        self.retriever = HybridRetriever(
            repository_name,
        )

        self.reranker = self.registry.get_reranker()

        # ========================================================
        # Existing generation components
        # ========================================================

        self.provider = self.registry.get_provider(
            "ollama",
        )

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        # ========================================================
        # Generic execution engine
        # ========================================================

        self.step_executor = StepExecutor(
            retriever=self.retriever,
            reranker=self.reranker,
            context_builder=self.context_builder,
            prompt_builder=self.prompt_builder,
            provider=self.provider,
        )

    # ============================================================
    # Public API
    # ============================================================

    def ask(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        """
        Backwards-compatible entry point.

        Existing callers can continue to use:

            pipeline.ask(request)

        Internally this now performs:

            Request
                ↓
            Planner
                ↓
            ExecutionPlan
                ↓
            execute()
        """

        planner_result = self.planner.plan(
            request.query,
        )

        return self.execute(
            request=request,
            plan=planner_result.execution_plan,
        )

    def execute(
        self,
        request: AgentRequest,
        plan: ExecutionPlan,
    ) -> AgentResponse:
        """
        Execute an already-created ExecutionPlan.

        This method deliberately does not make planning decisions.

        The caller supplies the plan, and the pipeline executes that
        plan through StepExecutor.

        This separation allows future callers to do:

            plan = planner.plan(...)
            pipeline.execute(request, plan)

        and eventually allows more advanced planning systems to
        construct ExecutionPlans independently.
        """

        Metrics.record_request()
        Metrics.increment_sessions()

        try:

            with Metrics.pipeline_timer():

                # ==================================================
                # Conversation Memory
                # ==================================================

                with Metrics.memory_read_timer():

                    history = self.memory.format_history(
                        request.session_id,
                    )

                # ==================================================
                # Execution Context
                # ==================================================

                execution_context = ExecutionContext(
                    request=request,
                    plan=plan,
                    conversation_history=history,
                )

                # Store useful top-level execution metadata.

                execution_context.set_metadata(
                    "repository_name",
                    self.repository_name,
                )

                execution_context.set_metadata(
                    "session_id",
                    request.session_id,
                )

                execution_context.set_metadata(
                    "task",
                    plan.task.value,
                )

                execution_context.set_metadata(
                    "planned_step_count",
                    len(plan.steps),
                )

                # ==================================================
                # Plan Execution
                # ==================================================

                execution_result = self.step_executor.execute_plan(
                    execution_context,
                )

                # ==================================================
                # Handle Execution Failure
                # ==================================================

                if not execution_result.success:

                    self._raise_execution_error(
                        execution_result,
                    )

                # ==================================================
                # Update Conversation Memory
                # ==================================================

                self._update_memory(
                    request=request,
                    execution_result=execution_result,
                )

                # ==================================================
                # Build Final Response
                # ==================================================

                return self._build_response(
                    execution_result,
                )

        except Exception:

            Metrics.record_error()

            raise

        finally:

            Metrics.decrement_sessions()

    # ============================================================
    # Memory
    # ============================================================

    def _update_memory(
        self,
        request: AgentRequest,
        execution_result: ExecutionResult,
    ) -> None:
        """
        Store the user request and generated assistant response
        in conversation memory.

        Memory is updated only after successful plan execution.
        """

        generation = execution_result.generation

        if generation is None:

            raise RuntimeError(
                "Execution completed successfully but produced " "no generation result."
            )

        with Metrics.memory_write_timer():

            self.memory.add_message(
                request.session_id,
                "user",
                request.query,
            )

            self.memory.add_message(
                request.session_id,
                "assistant",
                generation.response,
            )

    # ============================================================
    # Response
    # ============================================================

    def _build_response(
        self,
        execution_result: ExecutionResult,
    ) -> AgentResponse:
        """
        Convert the successful ExecutionResult into the existing
        public AgentResponse model.

        This keeps the API response independent from the internal
        execution architecture.
        """

        context = execution_result.context.context

        prompt = execution_result.context.prompt

        generation = execution_result.context.generation

        if context is None:

            raise RuntimeError("Execution completed without a context result.")

        if prompt is None:

            raise RuntimeError("Execution completed without a prompt result.")

        if generation is None:

            raise RuntimeError("Execution completed without a generation result.")

        return AgentResponse(
            answer=generation.response,
            retrieved_chunks=context.num_chunks,
            context_size=context.context_size,
            prompt_size=prompt.prompt_size,
            model_name=generation.model_name,
        )

    # ============================================================
    # Error Handling
    # ============================================================

    @staticmethod
    def _raise_execution_error(
        execution_result: ExecutionResult,
    ) -> None:
        """
        Re-raise the original execution exception.

        Preserving the original exception is important because the
        previous AgentPipeline behavior propagated the actual error
        rather than wrapping everything in a generic exception.
        """

        if execution_result.error is not None:

            raise execution_result.error

        if execution_result.failed_step is not None:

            raise RuntimeError(
                "Execution failed at step "
                f"'{execution_result.failed_step.step_type.value}'."
            )

        raise RuntimeError("Execution failed without an associated error.")
