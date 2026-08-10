from enum import Enum

from pydantic import BaseModel


class StepType(str, Enum):

    RETRIEVE = "retrieve"

    RERANK = "rerank"

    BUILD_CONTEXT = "build_context"

    BUILD_PROMPT = "build_prompt"

    GENERATE = "generate"

    REVIEW = "review"

    EXECUTE = "execute"

    PATCH = "patch"


class PlannerStep(BaseModel):

    order: int

    step_type: StepType

    description: str
