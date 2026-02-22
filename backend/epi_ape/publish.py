from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import MatchRecord, PaperRecord
from .utils import dump_json, ensure_dir


def _counts(matches: list[MatchRecord]) -> dict:
    ai_wins = 0
    human_wins = 0
    ties = 0

    for match in matches:
        if match.winner == "paperA":
            ai_wins += 1
        elif match.winner == "paperB":
            human_wins += 1
        else:
            ties += 1

    return {"aiWins": ai_wins, "humanWins": human_wins, "ties": ties}


def publish_web_data(
    web_data_dir: Path, papers: list[PaperRecord], matches: list[MatchRecord]
) -> None:
    ensure_dir(web_data_dir)

    papers_payload = [
        paper.to_web_dict()
        for paper in sorted(papers, key=lambda x: x.conservative_score(), reverse=True)
    ]
    dump_json(web_data_dir / "papers.json", papers_payload)

    counts = _counts(matches)
    recent = list(reversed(matches[-20:]))
    matches_payload = {
        "lastUpdated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "totalMatches": len(matches),
        "dailyMatches": 50,
        "aiVsHuman": counts,
        "recentMatches": [item.to_web_dict() for item in recent],
    }
    dump_json(web_data_dir / "matches.json", matches_payload)
