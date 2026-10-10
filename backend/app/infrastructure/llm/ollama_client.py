"""Small injectable Ollama adapter; no models or network calls on import."""
import json
import math
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def validate_vectors(vectors, expected_count, dimension=None):
    if not isinstance(vectors, list) or len(vectors) != expected_count:
        raise ValueError("Embedding response count does not match input count")
    for vector in vectors:
        if not isinstance(vector, list) or not vector:
            raise ValueError("Embedding vectors must be nonempty lists")
        if dimension is None:
            dimension = len(vector)
        if len(vector) != dimension:
            raise ValueError("Embedding vector dimensions do not match")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
                   and math.isfinite(v) for v in vector):
            raise ValueError("Embedding vectors must contain finite numbers")
        if not any(vector):
            raise ValueError("Zero embedding vectors cannot be compared")
    return dimension


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", embedding_model="bge-m3",
                 generation_model="llama3.2", timeout=120, transport=None):
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username:
            raise ValueError("Ollama URL must be an HTTP(S) address without credentials")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        self.base_url = base_url.rstrip("/")
        self.embedding_model = embedding_model
        self.generation_model = generation_model
        self.timeout = timeout
        self.transport = transport or self._post

    def _post(self, endpoint, payload):
        request = Request(self.base_url + endpoint, data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read(16 * 1024 * 1024 + 1)
                if len(raw) > 16 * 1024 * 1024:
                    raise ValueError("Ollama response exceeds 16 MiB")
                data = json.loads(raw)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError("Ollama request failed; check server, models, and timeout") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Ollama returned invalid JSON") from exc
        if not isinstance(data, dict) or data.get("error"):
            raise RuntimeError("Ollama returned an invalid response or model error")
        return data

    def embed(self, texts):
        if not texts or any(not isinstance(t, str) or not t.strip() for t in texts):
            raise ValueError("Embedding input must contain nonempty text")
        data = self.transport("/api/embed", {"model": self.embedding_model, "input": texts})
        vectors = data.get("embeddings") if isinstance(data, dict) else None
        validate_vectors(vectors, len(texts))
        return vectors

    def generate(self, prompt):
        data = self.transport("/api/generate", {
            "model": self.generation_model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0},
        })
        answer = data.get("response") if isinstance(data, dict) else None
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Ollama returned no answer text")
        return answer
