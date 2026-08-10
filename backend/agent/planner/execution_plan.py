from enum import Enum

from pydantic import BaseModel

from backend.agent.planner.planner_step import PlannerStep


class TaskType(str, Enum):

    EXPLAIN = "explain"

    SEARCH = "search"

    GENERATE = "generate"

    REFACTOR = "refactor"

    TEST = "test"

    EXECUTE = "execute"

    CHAT = "chat"

    UNKNOWN = "unknown"


class ExecutionPlan(BaseModel):

    task: TaskType

    steps: list[PlannerStep]

    requires_retrieval: bool = True

    requires_generation: bool = True

    requires_execution: bool = False

    requires_review: bool = False
