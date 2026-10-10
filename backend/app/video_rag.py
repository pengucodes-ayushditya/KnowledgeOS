"""KnowledgeOS local video/audio RAG CLI: python -m app.video_rag --help."""
import argparse
import json
import os
from pathlib import Path
import sys

from app.domains.ingestion.schemas.transcript import parse_transcript
from app.domains.ingestion.services.media_service import extract_audio, transcribe_audio
from app.domains.ingestion.services.transcript_service import merge_chunks
from app.domains.retrieval.services.video_rag_service import VideoRAGService
from app.infrastructure.llm.ollama_client import OllamaClient
from app.infrastructure.storage.rag_index import read_json, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description="KnowledgeOS timestamped local video RAG")
    commands = parser.add_subparsers(dest="command", required=True)
    extract = commands.add_parser("extract", help="Extract audio from a local video using FFmpeg")
    extract.add_argument("source", type=Path)
    extract.add_argument("output", type=Path)
    extract.add_argument("--overwrite", action="store_true")
    transcribe = commands.add_parser("transcribe", help="Transcribe each local audio file")
    transcribe.add_argument("sources", nargs="+", type=Path)
    transcribe.add_argument("--output-dir", required=True, type=Path)
    transcribe.add_argument("--model", default="base")
    transcribe.add_argument("--model-cache", type=Path,
                            default=os.environ.get("WHISPER_CACHE_DIR", "../rag-data/whisper-models"),
                            help="Directory for downloaded Whisper model weights")
    transcribe.add_argument("--language", help="Language code; omitted means automatic detection")
    transcribe.add_argument("--task", choices=["transcribe", "translate"], default="transcribe")
    transcribe.add_argument("--overwrite", action="store_true")
    index = commands.add_parser("index", help="Merge transcript segments and build a JSON vector index")
    index.add_argument("transcripts", nargs="+", type=Path)
    index.add_argument("--output", required=True, type=Path)
    index.add_argument("--group-size", type=int, default=5)
    index.add_argument("--batch-size", type=int, default=32)
    index.add_argument("--overwrite", action="store_true")
    query = commands.add_parser("query", help="Answer using timestamped transcript evidence")
    query.add_argument("index", type=Path)
    query.add_argument("question")
    query.add_argument("--top-k", type=int, default=3)
    query.add_argument("--min-similarity", type=float, default=0.0)
    query.add_argument("--generation-model", default="llama3.2")
    for command in (index, query):
        command.add_argument("--ollama-url", default=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"))
        command.add_argument("--embedding-model", default=os.environ.get("EMBEDDING_MODEL", "bge-m3"))
        command.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args(argv)
    try:
        if args.command == "extract":
            print(extract_audio(args.source, args.output, args.overwrite))
        elif args.command == "transcribe":
            outputs = transcribe_audio(args.sources, args.output_dir, args.model,
                                       args.language, args.task, args.overwrite,
                                       model_cache=args.model_cache)
            print(json.dumps([str(p) for p in outputs]))
        else:
            client = OllamaClient(args.ollama_url, args.embedding_model,
                                  getattr(args, "generation_model", "llama3.2"), args.timeout)
            service = VideoRAGService(client)
            if args.command == "index":
                if args.output.exists() and not args.overwrite:
                    raise FileExistsError("Output exists; choose a new path or use --overwrite")
                if args.output.resolve() in {p.resolve() for p in args.transcripts}:
                    raise ValueError("Index output must differ from transcript inputs")
                chunks = []
                for path in args.transcripts:
                    chunks.extend(merge_chunks(parse_transcript(read_json(path), path.stem), args.group_size))
                write_json(args.output, service.build_index(chunks, args.batch_size), args.overwrite)
                print(json.dumps({"index": str(args.output), "chunks": len(chunks)}))
            else:
                print(json.dumps(service.answer(read_json(args.index), args.question,
                                                 args.top_k, args.min_similarity),
                                 ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(f"Video RAG failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
