from backend.generation.providers.ollama_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def __init__(
        self,
        model=None,
    ):