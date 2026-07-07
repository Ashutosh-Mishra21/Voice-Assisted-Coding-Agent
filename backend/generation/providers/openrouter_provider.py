from backend.generation.providers.openai_provider import BaseProvider

class OpenRouterProvider(BaseProvider):

    def __init__(
        self,
        model=None,
    ):