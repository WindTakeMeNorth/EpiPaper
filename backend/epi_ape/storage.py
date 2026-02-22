from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import MatchRecord, PaperRecord
from .utils import dump_json, ensure_dir, load_json


@dataclass
class StateStore:
    state_dir: Path

    @property
    def papers_path(self) -> Path:
        return self.state_dir / "papers.json"

    @property
    def matches_path(self) -> Path:
        return self.state_dir / "matches.json"

    @property
    def meta_path(self) -> Path:
        return self.state_dir / "meta.json"

    def init_dirs(self) -> None:
        ensure_dir(self.state_dir)

    def load_papers(self) -> list[PaperRecord]:
        raw = load_json(self.papers_path, default=[])
        return [PaperRecord.from_dict(item) for item in raw]

    def save_papers(self, papers: list[PaperRecord]) -> None:
        dump_json(self.papers_path, [paper.to_state_dict() for paper in papers])

    def load_matches(self) -> list[MatchRecord]:
        raw = load_json(self.matches_path, default=[])
        return [MatchRecord.from_dict(item) for item in raw]

    def save_matches(self, matches: list[MatchRecord]) -> None:
        dump_json(self.matches_path, [match.to_state_dict() for match in matches])

    def load_meta(self) -> dict:
        return load_json(self.meta_path, default={})

    def save_meta(self, meta: dict) -> None:
        dump_json(self.meta_path, meta)
