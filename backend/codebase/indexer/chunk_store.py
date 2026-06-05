import json
from pathlib import Path

from backend.config.paths import (
    INDEXES_DIR,
)


class ChunkStore:

    def save_chunks(
        self,
        repo_name: str,
        chunks: list,
    ):

        output_file = INDEXES_DIR / f"{repo_name}_chunks.json"

        data = [chunk.model_dump() for chunk in chunks]

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
            )

        return output_file

    def load_chunks(
        self,
        repo_name: str,
    ):

        input_file = INDEXES_DIR / f"{repo_name}_chunks.json"

        if not input_file.exists():

            return []

        with open(
            input_file,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)
