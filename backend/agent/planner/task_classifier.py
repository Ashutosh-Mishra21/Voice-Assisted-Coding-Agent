from backend.agent.planner.execution_plan import (
    TaskType,
)


class TaskClassifier:

    EXPLAIN = {
        "explain",
        "describe",
        "how",
        "why",
        "understand",
    }

    SEARCH = {
        "find",
        "locate",
        "search",
        "where",
    }

    GENERATE = {
        "generate",
        "create",
        "implement",
        "add",
        "write",
    }

    REFACTOR = {
        "refactor",
        "rename",
        "improve",
        "cleanup",
    }

    TEST = {
        "test",
        "pytest",
        "unit test",
        "integration",
    }

    EXECUTE = {
        "run",
        "execute",
        "build",
        "install",
    }

    def classify(
        self,
        query: str,
    ) -> TaskType:

        query = query.lower()

        for word in self.EXPLAIN:

            if word in query:

                return TaskType.EXPLAIN

        for word in self.SEARCH:

            if word in query:

                return TaskType.SEARCH

        for word in self.GENERATE:

            if word in query:

                return TaskType.GENERATE

        for word in self.REFACTOR:

            if word in query:

                return TaskType.REFACTOR

        for word in self.TEST:

            if word in query:

                return TaskType.TEST

        for word in self.EXECUTE:

            if word in query:

                return TaskType.EXECUTE

        return TaskType.CHAT
