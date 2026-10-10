"""Import and merge transcript segments without import-time processing."""
from app.domains.ingestion.schemas.transcript import TranscriptChunk


def merge_chunks(chunks, group_size=5):
    if not isinstance(group_size, int) or isinstance(group_size, bool) or group_size < 1:
        raise ValueError("group_size must be a positive integer")
    merged, group = [], []

    def flush():
        if group:
            merged.append(TranscriptChunk(
                source_id=group[0].source_id, title=group[0].title,
                start=group[0].start, end=max(c.end for c in group),
                text=" ".join(c.text.strip() for c in group),
            ))
            group.clear()

    previous = None
    for chunk in chunks:
        identity = (chunk.source_id, chunk.title)
        if previous and identity == (previous.source_id, previous.title):
            if chunk.start < previous.start:
                raise ValueError("Segments within a source must be chronological")
        if group and identity != (group[0].source_id, group[0].title):
            flush()
        group.append(chunk)
        if len(group) == group_size:
            flush()
        previous = chunk
    flush()
    return merged
