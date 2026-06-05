import uuid

from backend.models.code_chunk import CodeChunk


class ChunkBuilder:

    def build_chunks(
        self,
        file_path: str,
        content: str,
        symbols: list,
    ):

        chunks = []

        lines = content.splitlines()

        for symbol in symbols:

            start = symbol["start_line"]
            end = symbol["end_line"]

            chunk_text = "\n".join(lines[start - 1 : end])

            chunk = CodeChunk(
                chunk_id=str(uuid.uuid4()),
                file_path=file_path,
                language="python",
                chunk_type=symbol["type"],
                symbol_name=symbol["name"],
                start_line=start,
                end_line=end,
                content=chunk_text,
            )

            chunks.append(chunk)

        return chunks
