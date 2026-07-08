from backend.monitoring.metrics import (
    ACTIVE_SESSIONS,
    CONTEXT_DURATION,
    CONTEXT_SIZE_BYTES,
    GENERATION_DURATION,
    MEMORY_DURATION,
    PIPELINE_DURATION,
    PROMPT_DURATION,
    PROMPT_SIZE_BYTES,
    REQUEST_ERRORS_TOTAL,
    REQUESTS_TOTAL,
    RERANK_DURATION,
    RETRIEVAL_DURATION,
    RETRIEVED_CHUNKS_COUNT,
)


class Metrics:

    # ==================================================
    # Request Metrics
    # ==================================================

    @staticmethod
    def record_request():

        REQUESTS_TOTAL.inc()

    @staticmethod
    def record_error():

        REQUEST_ERRORS_TOTAL.inc()

    @staticmethod
    def increment_sessions():

        ACTIVE_SESSIONS.inc()

    @staticmethod
    def decrement_sessions():

        ACTIVE_SESSIONS.dec()

    # ==================================================
    # Timers
    # ==================================================

    @staticmethod
    def pipeline_timer():

        return PIPELINE_DURATION.time()

    @staticmethod
    def memory_timer():

        return MEMORY_DURATION.time()

    @staticmethod
    def retrieval_timer():

        return RETRIEVAL_DURATION.time()

    @staticmethod
    def rerank_timer():

        return RERANK_DURATION.time()

    @staticmethod
    def context_timer():

        return CONTEXT_DURATION.time()

    @staticmethod
    def prompt_timer():

        return PROMPT_DURATION.time()

    @staticmethod
    def generation_timer():

        return GENERATION_DURATION.time()

    # ==================================================
    # Sizes
    # ==================================================

    @staticmethod
    def record_context_size(
        size: int,
    ):

        CONTEXT_SIZE_BYTES.observe(size)

    @staticmethod
    def record_prompt_size(
        size: int,
    ):

        PROMPT_SIZE_BYTES.observe(size)

    @staticmethod
    def record_retrieved_chunks(
        chunks: int,
    ):

        RETRIEVED_CHUNKS_COUNT.observe(chunks)
