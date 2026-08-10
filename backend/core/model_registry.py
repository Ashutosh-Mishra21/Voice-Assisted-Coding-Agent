from threading import Lock

from backend.config.settings import settings

from backend.retrieval.semantic.embedder import Embedder
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

    # =====================================================
    # Embedder
    # =====================================================

    def get_embedder(self):

        if self._embedder is None:
            self._embedder = Embedder()

        return self._embedder

    # =====================================================
    # Reranker
    # =====================================================

    def get_reranker(self):

        if self._reranker is None:
            self._reranker = CrossEncoderReranker()

        return self._reranker

    # =====================================================
    # Providers
    # =====================================================

    def get_provider(
        self,
        provider_name: str = None,
    ):

        provider_name = (provider_name or settings.DEFAULT_PROVIDER).lower()

        if provider_name in self._providers:
            return self._providers[provider_name]

        # -------------------------------
        # Ollama
        # -------------------------------

        if provider_name == "ollama":
            instance = OllamaProvider(
                model=settings.OLLAMA_MODEL,
                host=settings.OLLAMA_HOST,
            )

        # -------------------------------
        # OpenAI
        # -------------------------------

        elif provider_name == "openai":
            instance = OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
            )

        # -------------------------------
        # OpenRouter
        # -------------------------------

        elif provider_name == "openrouter":
            instance = OpenRouterProvider(
                api_key=settings.OPENROUTER_API_KEY,
                model=settings.OPENROUTER_MODEL,
            )

        else:
            raise ValueError(f"Unsupported provider: {provider_name}")

        self._providers[provider_name] = instance

        return instance

    # =====================================================
    # Cleanup
    # =====================================================

    def unload(self):

        self._embedder = None
        self._reranker = None
        self._providers.clear()
