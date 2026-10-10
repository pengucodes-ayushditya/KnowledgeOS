import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from app.domains.ingestion.schemas.transcript import TranscriptChunk, parse_transcript
from app.domains.ingestion.services.media_service import extract_audio, transcribe_audio
from app.domains.ingestion.services.transcript_service import merge_chunks
from app.domains.retrieval.services.video_rag_service import VideoRAGService
from app.infrastructure.llm.ollama_client import OllamaClient, validate_vectors
from app.infrastructure.storage.rag_index import read_json, write_json


class VideoRAGTests(unittest.TestCase):
    def chunk(self, source="lecture", start=0, text="history", end=None):
        return TranscriptChunk(source, source, start, start + 1 if end is None else end, text)

    def client(self):
        def transport(endpoint, data):
            if endpoint == "/api/embed":
                return {"embeddings": [[1., 0.] if text == "history" else [0., 1.]
                                       for text in data["input"]]}
            return {"response": "History is discussed in lecture [S1]."}
        return OllamaClient(transport=transport)

    def test_merge_preserves_last_partial_group_and_sources(self):
        chunks = [self.chunk(start=i) for i in range(7)] + [self.chunk("other")]
        merged = merge_chunks(chunks, 5)
        self.assertEqual([(c.source_id, c.start, c.end) for c in merged],
                         [("lecture", 0, 5), ("lecture", 5, 7), ("other", 0, 1)])

    def test_invalid_timestamps_and_order_rejected(self):
        for start, end in [(3, 1), (-1, 1), (float("nan"), 1)]:
            with self.assertRaises(ValueError): self.chunk(start=start, end=end)
        with self.assertRaises(ValueError):
            merge_chunks([self.chunk(start=2), self.chunk(start=1)])

    def test_legacy_transcript_import(self):
        chunks = parse_transcript({"chunks": [{"number": "1", "title": "History",
                                  "start": 4, "end": 8, "text": "history"}]}, "video1")
        self.assertEqual((chunks[0].source_id, chunks[0].title), ("video1", "History"))
        with self.assertRaises(ValueError): parse_transcript({"chunks": []}, "empty")

    def test_index_query_json_roundtrip_and_timestamped_sources(self):
        service = VideoRAGService(self.client())
        index = service.build_index([self.chunk(start=10), self.chunk("science", text="science")], 1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "index.json"
            write_json(path, index)
            answer = service.answer(read_json(path), "history", top_k=1)
        self.assertEqual(answer["sources"][0]["citation"], "S1")
        self.assertEqual(answer["sources"][0]["start"], 10)
        self.assertEqual(answer["sources"][0]["source_id"], "lecture")

    def test_no_evidence_skips_generation(self):
        client = self.client()
        service = VideoRAGService(client)
        index = service.build_index([self.chunk(text="science")])
        client.generate = Mock(side_effect=AssertionError("Must not generate"))
        self.assertEqual(service.answer(index, "history", min_similarity=.5)["sources"], [])

    def test_model_and_dimension_mismatch_rejected(self):
        service = VideoRAGService(self.client())
        index = service.build_index([self.chunk()])
        index["embedding_model"] = "other"
        with self.assertRaises(ValueError): service.retrieve(index, "history")
        index["embedding_model"] = "bge-m3"
        index["dimension"] = 3
        with self.assertRaises(ValueError): service.retrieve(index, "history")

    def test_malformed_embeddings_fail(self):
        for vectors in [[], [[0, 0]], [[1, float("inf")]], [[1], [1, 2]]]:
            with self.assertRaises(ValueError): validate_vectors(vectors, max(1, len(vectors)))
        client = OllamaClient(transport=lambda *args: {"embeddings": [[1., 0.]]})
        with self.assertRaises(ValueError): client.embed(["one", "two"])

    def test_outputs_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            write_json(path, {"original": True})
            with self.assertRaises(FileExistsError): write_json(path, {"original": False})
            self.assertTrue(read_json(path)["original"])

    def test_every_audio_file_gets_a_transcript(self):
        model = Mock()
        model.transcribe.return_value = {"segments": [{"start": 0, "end": 2, "text": "history"}],
                                         "language": "en"}
        with tempfile.TemporaryDirectory() as folder:
            inputs = [Path(folder) / name for name in ["first.wav", "second.wav"]]
            for path in inputs: path.write_bytes(b"test fixture; mock transcription")
            outputs = transcribe_audio(inputs, Path(folder) / "jsons", model_loader=lambda _: model)
            self.assertEqual([read_json(p)["chunks"][0]["source_id"] for p in outputs], ["first", "second"])
            self.assertEqual(model.transcribe.call_count, 2)

    def test_whisper_model_uses_explicit_local_cache(self):
        whisper = Mock()
        whisper.load_model.return_value.transcribe.return_value = {
            "segments": [{"start": 0, "end": 2, "text": "fixture"}], "language": "en"}
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "fixture.wav"
            source.touch()
            cache = Path(folder) / "models"
            with patch.dict("sys.modules", {"whisper": whisper}):
                transcribe_audio([source], Path(folder) / "jsons", model_cache=cache)
            whisper.load_model.assert_called_once_with("base", download_root=str(cache))

    def test_checked_ffmpeg_failure_and_argument_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / "with spaces.mp4", Path(folder) / "audio.wav"
            source.touch()
            runner = Mock(side_effect=subprocess.CalledProcessError(1, "ffmpeg"))
            with self.assertRaises(RuntimeError): extract_audio(source, output, runner=runner)
            args, kwargs = runner.call_args
            self.assertIn(str(source), args[0])
            self.assertTrue(kwargs["check"])


if __name__ == "__main__":
    unittest.main()
