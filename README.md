# KnowledgeOS

**A local video/audio RAG prototype with a FastAPI workspace backend.**

KnowledgeOS converts local lecture recordings into searchable, timestamped text.
It uses Whisper for transcription, Ollama for embeddings and answer generation,
and returns source titles and time ranges alongside answers. The repository
consolidates the standalone lecture RAG implementation with the KnowledgeOS backend.

## Implemented functionality

- Extract mono audio from a local video with FFmpeg.
- Transcribe multiple audio files, or request English translation, with Whisper.
- Import timestamped transcript JSON and merge consecutive segments.
- Build a versioned JSON embedding index using Ollama `bge-m3`.
- Retrieve transcript chunks by cosine similarity and generate answers using `llama3.2`.
- Return structured source IDs, titles, citation labels, similarity scores, and time ranges.
- Create and list workspaces through FastAPI.

## Backend scope

The backend includes SQLAlchemy models, repositories, and an Alembic migration
for workspaces, resources, documents, chunks, embeddings, and associated knowledge
records. These are a **partial database implementation**, not an operational
extraction or reasoning pipeline. Only workspace creation/listing is exposed by
the API. The video/audio RAG workflow runs through the CLI and stores indexes in
local JSON files; it does not persist its results into pgvector or workspace records.

## Setup

Use Python 3.11 and [uv](https://docs.astral.sh/uv/). From `backend/`:

```bash
uv sync --locked --extra media
source .venv/bin/activate
python -m app.video_rag --help
```

Install FFmpeg and Ollama separately. Start Ollama and make the models available:

```bash
ollama serve
```

In another terminal:

```bash
ollama pull bge-m3
ollama pull llama3.2
```

Whisper downloads its selected weights on first use. The default model is `base`;
weights are cached under ignored `rag-data/whisper-models/` when running from
`backend/`. Use `--model tiny.en` for the smaller English-only model.

## Video/audio workflow

Run these commands from `backend/` with media you are authorized to process:

```bash
python -m app.video_rag extract /path/to/lecture.mp4 ../rag-data/audio/lecture.wav
python -m app.video_rag transcribe ../rag-data/audio/lecture.wav \
  --output-dir ../rag-data/transcripts
python -m app.video_rag index ../rag-data/transcripts/lecture.json \
  --output ../rag-data/index.json
python -m app.video_rag query ../rag-data/index.json "What does the lecture explain?"
```

The input is a local recording; no YouTube downloader is included. Language is
automatically detected unless a code such as `--language hi` is supplied.
`--task translate` requests translation into English. Output files are protected
against replacement unless `--overwrite` is specified.

To try indexing without an audio recording, use the fabricated example:

```bash
python -m app.video_rag index ../examples/synthetic-transcript.json \
  --output ../rag-data/example-index.json
python -m app.video_rag query ../rag-data/example-index.json "What is spaced repetition?"
```

See [video RAG details](backend/docs/video-rag.md) for input formats and options.

## Workspace API

The local Compose configuration requires your own database password. At the
repository root, copy `.env.example` to `.env`, replace its placeholder, and run:

```bash
docker compose up -d postgres
```

From `backend/`, copy `.env.example` to `.env` and configure `DATABASE_URL` with
the same credentials. Replace the secret placeholder, then run:

```bash
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

Routes: `POST /api/v1/workspaces`, `GET /api/v1/workspaces`, `/`, and `/health`.
Interactive API documentation is available at `/docs`. `/health` reports process
liveness, not database or model readiness. The API has no authentication or tenant
isolation and is intended for local use.

## Validation

```bash
python -m unittest discover -s tests -v
```

The 15 automated tests cover transcript validation/merging, per-file transcription,
retrieval, index validation, protected writes, model-cache configuration, ORM
mapping, transaction behavior, and workspace HTTP creation/listing. Model calls
and transcription are mocked in this repeatable suite. Separate local smoke
checks exercised real FFmpeg, Whisper `tiny.en` and `base`, and Ollama embedding
and answer generation. These checks are not answer-quality or transcription
benchmarks. Workspace persistence tests use SQLite rather than live PostgreSQL.

## Limitations and data handling

- Answers can contain factual or citation errors. Inspect the returned evidence.
- Timestamp ranges identify retrieved chunks, not exact word locations.
- Similarity scores are ranking signals. `--min-similarity` is adjustable and
  does not reliably detect every unrelated question.
- JSON indexes use a linear scan and have a 64 MiB input limit.
- Rebuild indexes after changing embedding models. Model replacement under an
  unchanged name is not automatically detected.
- The default Ollama server is local. Configuring a remote server sends transcript
  text and questions to that server.
- Real recordings, lecture transcripts, embeddings, checkpoints, credentials,
  and local environments are excluded. Only fabricated example text is bundled.

## Layout

```text
backend/app/video_rag.py          Video/audio RAG CLI
backend/app/domains/ingestion/    Media processing, transcript formats, database records
backend/app/domains/retrieval/    Local video RAG service
backend/app/domains/workspace/    Workspace API and persistence
backend/app/domains/knowledge/    Database models and repositories
backend/app/infrastructure/       Ollama client and JSON storage
backend/alembic/                  Database migration
backend/tests/                   Automated tests
examples/                        Fabricated transcript
docker/                          Local PostgreSQL initialization
```
