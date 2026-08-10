from abc import ABC, abstractmethod

from backend.generation.prompts.prompt_result import PromptResult
from backend.generation.providers.provider_result import ProviderResult


class BaseProvider(ABC):

    def __init__(
        self,
        provider_name: str,
        model: str,
    ):
        self.provider_name = provider_name
        self.model = model

    @abstractmethod
    def generate(
        self,
        prompt: PromptResult,
    ) -> ProviderResult:
        raise NotImplementedError
