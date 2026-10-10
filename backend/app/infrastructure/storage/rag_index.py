"""Explicit, versioned JSON indexes; never deserialize prototype pickle files."""
import json
import os
from pathlib import Path
import tempfile


def read_json(path):
    path = Path(path)
    if path.stat().st_size > 64 * 1024 * 1024:
        raise ValueError("JSON input exceeds the local feature's 64 MiB limit")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data, overwrite=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
        if overwrite:
            os.replace(temporary, path)
        else:
            # Atomic create without silently replacing an existing index/transcript.
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
