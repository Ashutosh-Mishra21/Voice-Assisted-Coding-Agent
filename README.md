# Voice Assisted Coding Agent

A local-first coding assistant backend that is being built to understand a repository, retrieve the most relevant code context, generate answers with an LLM, and eventually connect that workflow to voice input/output and a VS Code extension.

The project is currently in an early but well-scaffolded stage. The strongest progress so far is in repository indexing, retrieval-augmented generation, provider abstraction, memory, monitoring, and FastAPI service structure. Voice, planning, safe code execution, and editor integration are prepared as modules but still need implementation.

## Project Goals

- Let a developer ask coding questions by voice or text.
- Index the current codebase and retrieve relevant files, classes, functions, and chunks.
- Build high-quality prompts from repository context and conversation memory.
- Generate answers through local or hosted LLM providers.
- Add future support for planning, editing, patching, test execution, review, and VS Code workflows.

## Current Progress

### Backend API

- FastAPI application entry point is available in `backend/main.py`.
- Root endpoint returns app name and version.
- Health endpoint is available at `GET /health`.
- Agent route namespace exists at `/agent`.
- `POST /agent/query` is currently a placeholder and still needs to be connected to the real agent pipeline.

### Repository Indexing

Implemented under `backend/codebase`.

- Repository scanner discovers supported source files.
- Python parsing is available through Tree-sitter.
- Symbol extraction is structured around classes and functions.
- Chunk building creates stable chunk IDs using file path, symbol metadata, and line ranges.
- Repository indexing combines scanning, parsing, symbol extraction, and chunk creation.

Current limitation:

- Only Python files are supported right now.

### Retrieval System

Implemented under `backend/retrieval`.

- Semantic retrieval module is scaffolded around embeddings and Qdrant.
- BM25 lexical retrieval is implemented with `rank-bm25`.
- Hybrid retrieval combines semantic and BM25 results.
- Reciprocal Rank Fusion is used to merge retrieval results.
- Cross-encoder reranking is implemented with Hugging Face Transformers.

Storage placeholders exist under:

- `storage/qdrant`
- `storage/bm25`
- `storage/indexes`
- `storage/embeddings`
- `storage/cache`

### Generation System

Implemented under `backend/generation`.

- Prompt builder creates repository-aware prompts.
- Context builder deduplicates chunks, groups them by file, includes conversation history, and respects a context budget.
- Provider abstraction exists for multiple LLM backends.
- Supported provider modules:
  - Ollama
  - OpenAI
  - OpenRouter

Default configuration currently points to:

- Provider: `ollama`
- Ollama model: `qwen3:8b`
- Embedding model: `BAAI/bge-small-en-v1.5`
- Reranker model: `BAAI/bge-reranker-base`

### Agent Pipeline

Implemented in `backend/agent/pipeline.py`.

The pipeline currently wires together:

1. Conversation memory lookup
2. Hybrid retrieval
3. Cross-encoder reranking
4. Context building
5. Prompt building
6. LLM generation
7. Conversation memory update
8. Metrics recording

This is one of the main foundations of the project, but it still needs to be exposed through the API route and connected to planner/executor modules.

### Memory

Implemented under `backend/agent/memory`.

- Redis-backed conversation storage exists.
- Session history can be loaded, appended, cleared, and formatted for prompt context.
- `MemoryManager` expects Redis to be running at `localhost:6379`.

### Monitoring

Implemented under `backend/monitoring`.

Metrics are available for:

- Total agent requests
- Request errors
- Active sessions
- Pipeline duration
- Memory read/write duration
- Retrieval duration
- Reranking duration
- Context building duration
- Prompt building duration
- Generation duration by provider/model
- Retrieved chunk counts
- Context and prompt sizes

### Planning, Execution, Coder, and Reviewer Modules

The following module areas already exist as packages but are mostly placeholders:

- `backend/agent/planner`
- `backend/agent/coder`
- `backend/agent/executor`
- `backend/agent/reviewer`
- `backend/execution`

Open planner files currently include:

- `execution_plan.py`
- `task_classifier.py`
- `planner_step.py`
- `planner_result.py`
- `planner.py`

These files are ready for the next stage: task classification, multi-step planning, tool selection, patch generation, command execution, test running, and review loops.

### Voice Modules

Voice package structure exists under `backend/voice`.

- `backend/voice/stt`
- `backend/voice/tts`

These modules are currently placeholders. Speech-to-text and text-to-speech integration are planned future work.

### VS Code Extension

A `vscode-extension` directory exists with TypeScript config and extension files, but the extension implementation is still empty. This is intended to become the editor-facing layer for sending prompts, receiving answers, triggering voice workflows, and applying patches.

## Project Structure

```text
backend/
  agent/             Agent pipeline, memory, planner/coder/executor/reviewer packages
  api/               FastAPI routes and middleware
  codebase/          Repository scanning, parsing, symbol extraction, chunking, indexing
  config/            Application settings and paths
  core/              Shared managers and model registry
  execution/         Future command, diff, patch, and test execution modules
  generation/        Context building, prompt building, and LLM providers
  monitoring/        Metrics, health, middleware, exporter scaffolding
  retrieval/         BM25, semantic, hybrid retrieval, fusion, reranking
  voice/             Future STT/TTS modules

local_models/        Placeholder folders for embeddings, reranker, and Whisper models
playground/          Sample repository for development experiments
scripts/            Manual indexing and pipeline test scripts
storage/            Local indexes, Qdrant data, cache, sessions, graphs
tests/              Test package structure
vscode-extension/   Future VS Code extension
```

## Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root if you want to override defaults:

```env
APP_NAME="Voice Assisted Coding Agent"
APP_VERSION="0.1.0"
HOST="127.0.0.1"
PORT=8000

DEFAULT_PROVIDER="ollama"
OLLAMA_HOST="http://localhost:11434"
OLLAMA_MODEL="qwen3:8b"

OPENAI_API_KEY=""
OPENAI_MODEL="gpt-4.1"

OPENROUTER_API_KEY=""
OPENROUTER_MODEL="deepseek/deepseek-chat"

QDRANT_COLLECTION="repository_chunks"
```

Start required local services as needed:

- Redis for conversation memory
- Ollama for local model generation

Run the backend:

```bash
python -m backend.main
```

Or:

```bash
uvicorn backend.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`

## Development Scripts

The `scripts` directory contains manual testing and development helpers for:

- Agent pipeline experiments
- Context builder tests
- Prompt builder tests
- Generation tests
- Memory tests
- BM25 indexing/search
- Semantic indexing/search
- Hybrid retrieval
- Reranking

These scripts are useful while the formal automated test suite is still being expanded.

## Current Limitations

- The public `/agent/query` API route is not yet connected to `AgentPipeline`.
- Planner files are currently empty and need implementation.
- Voice STT/TTS modules are placeholders.
- Execution, patching, testing, coder, and reviewer modules are placeholders.
- VS Code extension implementation is not yet built.
- Repository parsing currently supports Python only.
- Redis is required for memory, with no fallback memory store yet.
- Dependency list may need cleanup as provider modules require packages such as OpenAI, Ollama, and Prometheus client support.

## Roadmap

### Phase 1: Stabilize the Core Agent

- Connect `/agent/query` to `AgentPipeline`.
- Add request/response schemas for agent queries.
- Add repository selection to agent requests.
- Add graceful startup validation for Redis, Qdrant, model providers, and local model availability.
- Add error responses for missing indexes, missing providers, and unavailable services.
- Add automated tests for the pipeline with mocked retrieval, memory, and provider layers.

### Phase 2: Complete Planning

- Implement `TaskClassifier` to distinguish question answering, code explanation, bug fixing, refactoring, test generation, and command execution requests.
- Implement `PlannerStep`, `ExecutionPlan`, and `PlannerResult` models.
- Build a planner that converts user intent into ordered steps.
- Add plan validation before execution.
- Track planner decisions in logs and metrics.

### Phase 3: Add Code Editing and Execution

- Implement patch generation and application modules.
- Add diff preview and validation.
- Add command execution with allowlists and safety checks.
- Add test runner integration.
- Add rollback or recovery behavior for failed edits.
- Add a reviewer loop that checks generated patches before they are applied.

### Phase 4: Expand Repository Intelligence

- Support more languages such as JavaScript, TypeScript, Java, C++, Go, and Rust.
- Add file-level chunks for files without symbols.
- Build dependency graphs and call graphs under `storage/graphs`.
- Add incremental indexing with a file watcher.
- Improve chunk ranking with symbol type, file path, recency, and dependency proximity.

### Phase 5: Voice Assistant Layer

- Implement speech-to-text with Whisper or another local STT engine.
- Implement text-to-speech for assistant responses.
- Add wake-word or push-to-talk support.
- Add streaming partial transcription.
- Add voice confirmation before applying code changes or running commands.

### Phase 6: VS Code Extension

- Build a sidebar or chat panel.
- Send selected code, active file, and workspace metadata to the backend.
- Add commands for "Ask Agent", "Explain Selection", "Generate Tests", "Fix Error", and "Apply Patch".
- Display diffs before applying edits.
- Add voice controls inside the editor.

### Phase 7: Evaluation and Production Readiness

- Add benchmark tasks for retrieval quality.
- Add regression tests for prompt construction and context selection.
- Add integration tests for indexing, retrieval, generation, and memory.
- Add structured logging.
- Add authentication if the API is exposed beyond localhost.
- Add Docker Compose for backend, Redis, and optional supporting services.

## Suggested Next Milestone

The best next milestone is to make the text-based agent usable end to end:

1. Define agent request and response schemas.
2. Connect `POST /agent/query` to `AgentPipeline`.
3. Add a simple repository indexing command.
4. Add mocked tests for the agent route.
5. Verify a full question-answer flow against `playground/sample_repo`.

After that works reliably, voice and VS Code integration can be added on top of a stable core instead of trying to build every layer at once.
