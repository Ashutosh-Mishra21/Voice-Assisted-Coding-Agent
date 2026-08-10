from backend.agent.planner.execution_plan import (
    ExecutionPlan,
    TaskType,
)

from backend.agent.planner.planner_result import (
    PlannerResult,
)

from backend.agent.planner.planner_step import (
    PlannerStep,
    StepType,
)

from backend.agent.planner.task_classifier import (
    TaskClassifier,
)


class Planner:

    def __init__(self):

        self.classifier = TaskClassifier()

    def plan(
        self,
        query: str,
    ) -> PlannerResult:

        task = self.classifier.classify(query)

        steps = [
            PlannerStep(
                order=1,
                step_type=StepType.RETRIEVE,
                description="Retrieve relevant repository context",
            ),
            PlannerStep(
                order=2,
                step_type=StepType.RERANK,
                description="Rerank retrieved chunks",
            ),
            PlannerStep(
                order=3,
                step_type=StepType.BUILD_CONTEXT,
                description="Assemble repository context",
            ),
            PlannerStep(
                order=4,
                step_type=StepType.BUILD_PROMPT,
                description="Construct LLM prompt",
            ),
            PlannerStep(
                order=5,
                step_type=StepType.GENERATE,
                description="Generate response",
            ),
        ]

        plan = ExecutionPlan(
            task=task,
            steps=steps,
        )

        return PlannerResult(
            query=query,
            execution_plan=plan,
            reasoning=f"Task classified as {task.value}",
        )
