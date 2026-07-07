from backend.agent.memory.memory_manager import (
    MemoryManager,
)


def main():
    session_id = "test-session"

    memory = MemoryManager()

    # start clean for repeatable tests
    memory.clear_history(session_id)

    memory.add_message(
        session_id,
        "user",
        "Explain authentication.",
    )

    memory.add_message(
        session_id,
        "assistant",
        "Authentication is handled by AuthService.",
    )

    history = memory.get_history(session_id)

    print("\n" + "=" * 100)
    print("RAW HISTORY")
    print("=" * 100)
    print(history)

    print("\n" + "=" * 100)
    print("FORMATTED HISTORY")
    print("=" * 100)
    print(memory.format_history(session_id))


if __name__ == "__main__":
    main()
