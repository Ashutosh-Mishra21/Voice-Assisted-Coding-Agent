from backend.generation.context.context_result import (
    ContextResult,
)

from backend.generation.prompts.prompt_result import (
    PromptResult,
)

from backend.generation.prompts.system_prompts import (
    REPOSITORY_ASSISTANT_PROMPT,
)


class PromptBuilder:

    def build(
        self,
        context: ContextResult,
    ) -> PromptResult:

        user_prompt = f"""
Repository Context:

{context.context}

Answer the user's question using the repository context above.
""".strip()

        full_prompt = REPOSITORY_ASSISTANT_PROMPT + "\n\n" + user_prompt

        return PromptResult(
            system_prompt=REPOSITORY_ASSISTANT_PROMPT,
            user_prompt=user_prompt,
            full_prompt=full_prompt,
            prompt_size=len(full_prompt),
        )
