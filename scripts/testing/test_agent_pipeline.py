from backend.agent.pipeline import (
    AgentPipeline,
)

from backend.agent.agent_request import (
    AgentRequest,
)
 
from backend.agent.memory.memory_manager import (
    MemoryManager,
)

from backend.core.model_registry import (
    ModelRegistry,
)


def main():

    # --------------------------------------------------
    # Shared Application Services
    # --------------------------------------------------

    registry = ModelRegistry()

    memory = MemoryManager()
    
    # --------------------------------------------------
    # Agent Pipeline
    # --------------------------------------------------

    pipeline = AgentPipeline(
        repository_name="sample_repo",
        registry=registry,
        memory=memory,
    )

    # --------------------------------------------------
    # Test Request
    # --------------------------------------------------

    request = AgentRequest(
        session_id="session-001",
        repository_name="sample_repo",
        query="Explain how authentication works.",
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    response = pipeline.ask(request)

    # --------------------------------------------------
    # Print Response
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("AGENT RESPONSE")
    print("=" * 100)

    print(f"Model             : {response.model_name}")
    print(f"Retrieved Chunks  : {response.retrieved_chunks}")
    print(f"Context Size      : {response.context_size}")
    print(f"Prompt Size       : {response.prompt_size}")

    print("\n" + "=" * 100)
    print("ANSWER")
    print("=" * 100)

    print(response.answer)

    # --------------------------------------------------
    # Conversation Memory
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("CONVERSATION HISTORY")
    print("=" * 100)

    print(
        memory.format_history(
            request.session_id,
        )
    )

    from prometheus_client import generate_latest

    print("\n")
    print("=" * 100)
    print("PROMETHEUS METRICS")
    print("=" * 100)

    print(generate_latest().decode("utf-8"))


if __name__ == "__main__":
    main()
