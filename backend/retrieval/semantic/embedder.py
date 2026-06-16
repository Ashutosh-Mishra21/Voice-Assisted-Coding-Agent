from backend.core.embedding_manager import get_embedder


class Embedder:

    def __init__(self):

        self.model = get_embedder()

    def embed_texts(self, texts: list[str]):

        return self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=True
        )

    def embed_query(self, query: str):

        return self.model.encode(query, normalize_embeddings=True)
