from abc import ABC
from abc import abstractmethod

from backend.generation.prompts.prompt_result import (
    PromptResult,
)

from backend.generation.providers.provider_result import (
    ProviderResult,
)


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: PromptResult,
    ) -> ProviderResult:
        pass
