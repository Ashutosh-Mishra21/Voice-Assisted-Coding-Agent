from sentence_transformers import SentenceTransformer

from backend.config.settings import settings

_model = None


def get_embedder():

    global _model

    if _model is None:

        _model = SentenceTransformer(settings.EMBEDDING_MODEL)

    return _model
