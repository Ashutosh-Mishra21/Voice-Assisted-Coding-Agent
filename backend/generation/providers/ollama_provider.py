from ollama import Client

from backend.generation.prompts.prompt_result import (
    PromptResult,
)

from backend.generation.providers.base_provider import (
    BaseProvider,
)

from backend.generation.providers.provider_result import (
    ProviderResult,
)


class OllamaProvider(BaseProvider):

    def __init__(
        self,
        model: str = "qwen3:8b",
        host: str = "http://localhost:11434",
    ):

        super().__init__(
            provider_name="ollama",
            model=model,
        )

        self.client = Client(host=host)

    def generate(
        self,
        prompt: PromptResult,
    ) -> ProviderResult:

        response = self.client.chat(
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

        content = response["message"]["content"]

        return ProviderResult(
            response=content,
            model_name=self.model,
            provider_name=self.provider_name,
            prompt_size=prompt.prompt_size,
            completion_size=len(content),
            total_size=prompt.prompt_size + len(content),
        )
