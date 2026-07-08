from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram

# ==========================================================
# Requests
# ==========================================================

REQUESTS_TOTAL = Counter(
    "agent_requests_total",
    "Total number of agent requests",
)

REQUEST_ERRORS_TOTAL = Counter(
    "agent_request_errors_total",
    "Total number of failed agent requests",
)

ACTIVE_SESSIONS = Gauge(
    "agent_active_sessions",
    "Current active sessions",
)

# ==========================================================
# Pipeline Timing
# ==========================================================

PIPELINE_DURATION = Histogram(
    "pipeline_duration_seconds",
    "Entire agent pipeline execution time",
)

MEMORY_DURATION = Histogram(
    "memory_duration_seconds",
    "Conversation memory latency",
)

RETRIEVAL_DURATION = Histogram(
    "retrieval_duration_seconds",
    "Hybrid retrieval latency",
)

RERANK_DURATION = Histogram(
    "rerank_duration_seconds",
    "Cross encoder reranking latency",
)

CONTEXT_DURATION = Histogram(
    "context_build_duration_seconds",
    "Context building latency",
)

PROMPT_DURATION = Histogram(
    "prompt_build_duration_seconds",
    "Prompt construction latency",
)

GENERATION_DURATION = Histogram(
    "generation_duration_seconds",
    "LLM generation latency",
)

# ==========================================================
# Retrieval Quality
# ==========================================================

RETRIEVED_CHUNKS_COUNT = Histogram(
    "retrieved_chunks",
    "Number of retrieved chunks",
)

CONTEXT_SIZE_BYTES = Histogram(
    "context_size_bytes",
    "Context size in bytes",
)

PROMPT_SIZE_BYTES = Histogram(
    "prompt_size_bytes",
    "Prompt size in bytes",
)
