from sentence_transformers import SentenceTransformer

from backend.config.settings import settings


class Embedder:

    def __init__(self):

        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed_texts(self, texts: list[str]):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(self, query: str):

        return self.model.encode(
            query,
            normalize_embeddings=True,
        )
