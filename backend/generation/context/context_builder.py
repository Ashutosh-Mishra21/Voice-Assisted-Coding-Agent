from collections import defaultdict
from typing import List

from backend.generation.context.context_window import ContextWindow
from backend.generation.context.context_result import ContextResult


class ContextBuilder:
    """
    Builds repository context for LLM prompts.

    Responsibilities:

    - Deduplicate chunks
    - Group chunks by file
    - Add query metadata
    - Add conversation history
    - Respect context budget
    """

    def __init__(
        self,
        max_characters: int = 15000,
    ):
        self.window = ContextWindow(max_characters=max_characters)

    def build(
        self,
        query: str,
        retrieved_chunks: list,
        conversation_history: str | None = None,
    ) -> ContextResult:

        grouped = defaultdict(list)

        seen_chunks = set()

        for chunk in retrieved_chunks:

            if chunk.chunk_id in seen_chunks:
                continue

            seen_chunks.add(chunk.chunk_id)

            grouped[chunk.file_path].append(chunk)

        sections = []

        # --------------------------------------------------
        # USER QUERY
        # --------------------------------------------------

        sections.append("USER QUERY\n" "==========\n" f"{query}\n")

        # --------------------------------------------------
        # CONVERSATION HISTORY
        # --------------------------------------------------

        if conversation_history:

            sections.append(
                "\nCONVERSATION HISTORY\n"
                "====================\n"
                f"{conversation_history}\n"
            )

        # --------------------------------------------------
        # REPOSITORY CONTEXT
        # --------------------------------------------------

        sections.append("\nREPOSITORY CONTEXT\n" "==================\n")

        context = "\n".join(sections)

        current_size = len(context)

        for file_path, chunks in grouped.items():

            file_section = f"\nFILE: {file_path}\n" f"{'-' * 80}\n"

            if not self.window.fits(
                current_size,
                file_section,
            ):
                break

            context += file_section
            current_size = len(context)

            for chunk in chunks:

                symbol_section = (
                    f"\nSYMBOL: {chunk.symbol_name}\n"
                    f"{'~' * 40}\n"
                    f"{chunk.content}\n"
                )

                if not self.window.fits(
                    current_size,
                    symbol_section,
                ):
                    return ContextResult(
                        context=context,
                        query=query,
                        num_chunks=len(seen_chunks),
                        num_files=len(grouped),
                        context_size=current_size,
                    )

                context += symbol_section
                current_size = len(context)

        return ContextResult(
            context=context,
            query=query,
            num_chunks=len(seen_chunks),
            num_files=len(grouped),
            context_size=current_size,
        )
