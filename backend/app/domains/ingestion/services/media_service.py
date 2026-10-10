"""Optional local media adapters with checked conversion and lazy Whisper loading."""
from pathlib import Path
import subprocess

from app.domains.ingestion.schemas.transcript import TranscriptChunk
from app.infrastructure.storage.rag_index import write_json


def extract_audio(source, destination, overwrite=False, runner=subprocess.run):
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths must differ")
    if destination.exists() and not overwrite:
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        runner(["ffmpeg", "-nostdin", "-y" if overwrite else "-n", "-i", str(source),
                "-vn", "-ac", "1", "-ar", "16000", str(destination)],
               check=True, capture_output=True, timeout=600)
    except FileNotFoundError as exc:
        raise RuntimeError("Install FFmpeg and make ffmpeg available on PATH") from exc
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("FFmpeg conversion failed or timed out") from exc
    return destination


def transcribe_audio(sources, output_dir, model_name="base", language=None,
                     task="transcribe", overwrite=False, model_loader=None, model_cache=None):
    sources = [Path(p) for p in sources]
    if not sources:
        raise ValueError("Provide at least one audio file")
    if task not in {"transcribe", "translate"}:
        raise ValueError("task must be transcribe or translate")
    if len({p.stem for p in sources}) != len(sources):
        raise ValueError("Audio filenames must have unique stems in a batch")
    outputs = [Path(output_dir) / f"{p.stem}.json" for p in sources]
    for source, output in zip(sources, outputs):
        if not source.is_file():
            raise FileNotFoundError(source)
        if output.resolve() in {p.resolve() for p in sources}:
            raise ValueError("A transcript output would replace an input")
        if output.exists() and not overwrite:
            raise FileExistsError(output)
    if model_loader is None:
        try:
            import whisper
        except ImportError as exc:
            raise RuntimeError("Audio transcription requires optional openai-whisper") from exc
        cache = Path(model_cache) if model_cache else Path(output_dir).parent / "whisper-models"
        model_loader = lambda name: whisper.load_model(name, download_root=str(cache))
    model = model_loader(model_name)
    for source, output in zip(sources, outputs):
        result = model.transcribe(str(source), language=language, task=task,
                                  word_timestamps=False)
        chunks = [TranscriptChunk(source.stem, source.stem, s["start"], s["end"], s["text"])
                  for s in result["segments"] if s.get("text", "").strip()]
        if not chunks:
            raise ValueError(f"No speech segments returned for {source.name}")
        write_json(output, {"chunks": [c.to_dict() for c in chunks],
                            "language": result.get("language"), "task": task,
                            "transcription_model": model_name}, overwrite=overwrite)
    return outputs
