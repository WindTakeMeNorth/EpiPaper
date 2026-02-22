from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def seeded_random(key: str) -> random.Random:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    seed = int(digest[:16], 16)
    return random.Random(seed)


def now_compact() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return default

    return json.loads(text)


def dump_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def get_json(url: str, query: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    full_url = url
    if query:
        full_url = f"{url}?{urlencode(query)}"

    request = Request(
        full_url,
        headers={"User-Agent": "EPI-APE/0.1 (+https://github.com/)"},
    )

    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        text = response.read().decode(charset, errors="replace")

    return json.loads(text)
