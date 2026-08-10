from backend.agent.agent_request import (
    AgentRequest,
)

from backend.agent.agent_response import (
    AgentResponse,
)

from backend.agent.memory.memory_manager import (
    MemoryManager,
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
from backend.monitoring import Metrics


class AgentPipeline:
    def __init__(
        self,
        repository_name: str,
        registry: ModelRegistry,
        memory: MemoryManager,
    ):

        self.repository_name = repository_name

        self.memory = memory

        self.registry = registry

        self.retriever = HybridRetriever(repository_name)

        self.reranker = self.registry.get_reranker()

        self.provider = self.registry.get_provider("ollama")

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

    def ask(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        Metrics.record_request()
        Metrics.increment_sessions()

        try:
            with Metrics.pipeline_timer():

                # ==========================================
                # Conversation Memory
                # ==========================================

                with Metrics.memory_read_timer():
                    history = self.memory.format_history(request.session_id)

                # ==========================================
                # Hybrid Retrieval
                # ==========================================

                with Metrics.retrieval_timer():

                    retrieval_results = self.retriever.search(
                        query=request.query,
                        top_k=20,
                    )

                # ==========================================
                # Cross Encoder Reranking
                # ==========================================

                with Metrics.rerank_timer():

                    reranked = self.reranker.rerank(
                        query=request.query,
                        results=retrieval_results,
                        top_k=request.top_k,
                    )

                # ==========================================
                # Context Building
                # ==========================================

                with Metrics.context_timer():

                    context = self.context_builder.build(
                        query=request.query,
                        retrieved_chunks=reranked,
                        conversation_history=history,
                    )

                Metrics.record_context_size(context.context_size)
                Metrics.record_retrieved_chunks(context.num_chunks)

                # ==========================================
                # Prompt Building
                # ==========================================

                with Metrics.prompt_timer():

                    prompt = self.prompt_builder.build(
                        context=context,
                    )

                Metrics.record_prompt_size(prompt.prompt_size)

                # ==========================================
                # LLM Generation
                # ==========================================

                with Metrics.generation_timer(
                    provider=self.provider.provider_name,
                    model=self.provider.model,
                ):
                    generation = self.provider.generate(prompt)

                # ==========================================    
                # Update Conversation Memory
                # ==========================================

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

                return AgentResponse(
                    answer=generation.response,
                    retrieved_chunks=context.num_chunks,
                    context_size=context.context_size,
                    prompt_size=prompt.prompt_size,
                    model_name=generation.model_name,
                )

        except Exception:
            Metrics.record_error()
            raise

        finally:
            Metrics.decrement_sessions()
