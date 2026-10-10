"""Portable timestamped transcript format, including legacy prototype JSON."""
from dataclasses import asdict, dataclass
import math


@dataclass(frozen=True)
class TranscriptChunk:
    source_id: str
    title: str
    start: float
    end: float
    text: str

    def __post_init__(self):
        for field in ("source_id", "title", "text"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be nonempty text")
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
                   and math.isfinite(x) for x in (self.start, self.end)):
            raise ValueError("Timestamps must be finite numbers")
        if not 0 <= self.start <= self.end:
            raise ValueError("Expected 0 <= start <= end")

    def to_dict(self):
        return asdict(self)


def parse_transcript(data, source_id):
    if not isinstance(data, dict) or not isinstance(data.get("chunks"), list):
        raise ValueError("Transcript JSON needs a chunks list")
    chunks = []
    for item in data["chunks"]:
        if not isinstance(item, dict):
            raise ValueError("Each transcript chunk must be an object")
        chunks.append(TranscriptChunk(
            source_id=item.get("source_id", source_id),
            title=item.get("title", source_id),
            start=item.get("start"), end=item.get("end"), text=item.get("text"),
        ))
    if not chunks:
        raise ValueError("Transcript contains no chunks")
    return chunks
