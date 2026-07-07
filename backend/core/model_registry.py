from threading import Lock

from backend.retrieval.semantic.embedder import SemanticEmbedder
from backend.retrieval.rerank.reranker import CrossEncoderReranker

from backend.generation.providers.ollama_provider import OllamaProvider
from backend.generation.providers.openai_provider import OpenAIProvider
from backend.generation.providers.openrouter_provider import OpenRouterProvider


class ModelRegistry:

    _instance = None
    _lock = Lock()

    def __new__(cls):

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:

                    cls._instance = super().__new__(cls)

                    cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        self._embedder = None
        self._reranker = None
        self._providers = {}

    def get_embedder(self):

        if self._embedder is None:
            self._embedder = SemanticEmbedder()

        return self._embedder

    def get_reranker(self):

        if self._reranker is None:
            self._reranker = CrossEncoderReranker()

        return self._reranker

    def get_provider(
        self,
        provider: str = "ollama",
    ):
        provider = provider.lower()

        if provider in self._providers:

            return self._providers[provider]

        if provider == "ollama":
            instance = OllamaProvider()

        elif provider == "openai":
            instance = OpenAIProvider()

        elif provider == "openrouter":
            instance = OpenRouterProvider()

        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._providers[provider] = instance

        return instance

    def unload(self):

        self._embedder = None
        self._reranker = None
        self._providers.clear()
