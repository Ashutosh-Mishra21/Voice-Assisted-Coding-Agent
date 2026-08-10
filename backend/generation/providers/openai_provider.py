from openai import OpenAI

from backend.generation.prompts.prompt_result import (
    PromptResult,
)

from backend.generation.providers.base_provider import (
    BaseProvider,
)

from backend.generation.providers.provider_result import (
    ProviderResult,
)


class OpenAIProvider(BaseProvider):

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1",
    ):

        super().__init__(
            provider_name="openai",
            model=model,
        )

        self.client = OpenAI(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: PromptResult,
    ) -> ProviderResult:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt.system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt.user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        return ProviderResult(
            response=content,
            model_name=self.model,
            provider_name=self.provider_name,
            prompt_size=prompt.prompt_size,
            completion_size=len(content),
            total_size=prompt.prompt_size + len(content),
        )
