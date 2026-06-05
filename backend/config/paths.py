from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BACKEND_DIR = PROJECT_ROOT / "backend"

STORAGE_DIR = PROJECT_ROOT / "storage"

LOCAL_MODELS_DIR = PROJECT_ROOT / "local_models"

DOCS_DIR = PROJECT_ROOT / "docs"

TESTS_DIR = PROJECT_ROOT / "tests"


EMBEDDINGS_DIR = STORAGE_DIR / "embeddings"

INDEXES_DIR = STORAGE_DIR / "indexes"

BM25_DIR = STORAGE_DIR / "bm25"

GRAPHS_DIR = STORAGE_DIR / "graphs"

CACHE_DIR = STORAGE_DIR / "cache"

SESSIONS_DIR = STORAGE_DIR / "sessions"


for directory in [
    STORAGE_DIR,
    EMBEDDINGS_DIR,
    INDEXES_DIR,
    BM25_DIR,
    GRAPHS_DIR,
    CACHE_DIR,
    SESSIONS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
