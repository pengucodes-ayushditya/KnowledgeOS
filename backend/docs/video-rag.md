# Video/audio RAG

## Flow

Local recording → FFmpeg audio → Whisper transcript segments → segment merging
→ Ollama embeddings → JSON index → cosine retrieval → answer with source evidence.

The CLI does not require database settings. Its commands are `extract`,
`transcribe`, `index`, and `query`; each supports `--help`.

## Transcript format

```json
{"chunks": [{"source_id": "lecture-1", "title": "Example lecture", "start": 0, "end": 12, "text": "Example transcript text."}]}
```

`start` and `end` are seconds. Text, titles, and source IDs must be nonempty;
timestamps must be finite and chronological. Legacy prototype JSON with `number`,
`title`, `start`, `end`, and `text` is accepted; the filename stem supplies a source
ID when absent. Index original segments with default `--group-size 5`. For
already merged transcripts, use `--group-size 1`.

The implementation rebuilds embeddings from text and never loads pickle/joblib
artifacts. It has no import-time downloads, indexing, interactive prompts, or
automatic prompt/answer file writes.

## Options

- Transcription: `--model`, `--language`, `--task transcribe|translate`,
  `--model-cache`, and `--overwrite`. Multiple input paths are supported.
- Indexing: `--group-size`, `--batch-size`, `--output`, and `--overwrite`.
- Queries: `--top-k` (1–20), `--min-similarity` (−1 to 1), and `--generation-model`.
- Index/query connections: `--ollama-url`, `--embedding-model`, and `--timeout`.

`OLLAMA_BASE_URL` and `EMBEDDING_MODEL` environment variables supply defaults.
`WHISPER_CACHE_DIR` supplies the model-cache default. The CLI does not load `.env`
automatically. Defaults are Whisper `base`, embedding model `bge-m3`, generation
model `llama3.2`, three retrieved chunks, and minimum similarity 0.

The index records its version, embedding model, and vector dimension. Embedding
counts, dimensions, finite/nonzero values, and query model compatibility are
validated. Generation uses temperature 0, but correctness is not guaranteed.
Returned source records preserve the original time ranges independently of the
generated answer. All real transcript and index files should remain local.
