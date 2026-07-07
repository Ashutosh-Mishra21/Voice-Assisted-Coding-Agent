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


class AgentPipeline:
    def __init__(
        self,
        repository_name: str,
    ):

        self.repository_name = repository_name

        self.memory = MemoryManager()

        self.registry = ModelRegistry()

        self.retriever = HybridRetriever(repository_name)

        self.reranker = self.registry.get_reranker()

        self.provider = self.registry.get_provider("ollama")

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

    def ask(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        history = self.memory.format_history(request.session_id)
        retrieval_results = self.retriever.search(
            query=request.query,
            top_k=20,
        )
        reranked = self.reranker.rerank(
            query=request.query,
            results=retrieval_results,
            top_k=request.top_k,
        )

        context = self.context_builder.build(
            query=request.query,
            retrieved_chunks=reranked,
            conversation_history=history,
        )
        prompt = self.prompt_builder.build(context=context)
        generation = self.provider.generate(prompt)
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
