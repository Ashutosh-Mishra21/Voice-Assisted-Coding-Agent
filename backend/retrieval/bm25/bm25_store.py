import pickle

from backend.config.paths import BM25_DIR


class BM25Store:

    def save(
        self,
        repo_name: str,
        bm25_index,
        chunks,
    ):

        output_file = BM25_DIR / f"{repo_name}.pkl"

        data = {
            "index": bm25_index,
            "chunks": chunks,
        }

        with open(
            output_file,
            "wb",
        ) as f:

            pickle.dump(
                data,
                f,
            )

    def load(
        self,
        repo_name: str,
    ):

        input_file = BM25_DIR / f"{repo_name}.pkl"

        with open(
            input_file,
            "rb",
        ) as f:

            return pickle.load(f)
