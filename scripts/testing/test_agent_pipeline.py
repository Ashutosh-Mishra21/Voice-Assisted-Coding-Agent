from backend.agent.pipeline import (
    AgentPipeline,
)

from backend.agent.agent_request import (
    AgentRequest,
)


def main():

    pipeline = AgentPipeline(repository_name="sample_repo")

    request = AgentRequest(
        session_id="session-001",
        repository_name="sample_repo",
        query="Explain how authentication works.",
    )

    response = pipeline.ask(request)

    print("\n")
    print("=" * 100)
    print("AGENT RESPONSE")
    print("=" * 100)

    print(response)


if __name__ == "__main__":
    main()
