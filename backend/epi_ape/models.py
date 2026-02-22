from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class PaperRecord:
    id: str
    title: str
    source: str
    venue: str
    track: str
    method: str
    year: int
    paper_url: str

    status: str = "idea"
    advisor_passes: int = 0
    advisor_total: int = 0
    advisor_score: float = 0.0
    reviewer_score: float = 0.0
    review_recommendation: str = "pending"
    integrity_flags: list[str] = field(default_factory=list)

    mu: float = 25.0
    sigma: float = 8.333
    elo: int = 1500
    matches_played: int = 0

    contributor: str = "system"
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def conservative_score(self) -> float:
        return self.mu - 3 * self.sigma

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PaperRecord":
        return cls(
            id=payload["id"],
            title=payload["title"],
            source=payload["source"],
            venue=payload.get("venue", "Unknown"),
            track=payload.get("track", "Community Health"),
            method=payload.get("method", "Unknown"),
            year=int(payload.get("year", 2026)),
            paper_url=payload.get("paper_url", payload.get("paperUrl", "#")),
            status=payload.get("status", "idea"),
            advisor_passes=int(
                payload.get("advisor_passes", payload.get("advisorPasses", 0))
            ),
            advisor_total=int(
                payload.get("advisor_total", payload.get("advisorTotal", 0))
            ),
            advisor_score=float(
                payload.get("advisor_score", payload.get("advisorScore", 0.0))
            ),
            reviewer_score=float(
                payload.get("reviewer_score", payload.get("reviewerScore", 0.0))
            ),
            review_recommendation=payload.get(
                "review_recommendation", payload.get("reviewRecommendation", "pending")
            ),
            integrity_flags=list(
                payload.get("integrity_flags", payload.get("integrityFlags", []))
            ),
            mu=float(payload.get("mu", 25.0)),
            sigma=float(payload.get("sigma", 8.333)),
            elo=int(payload.get("elo", 1500)),
            matches_played=int(
                payload.get("matches_played", payload.get("matchesPlayed", 0))
            ),
            contributor=payload.get("contributor", "system"),
            created_at=payload.get(
                "created_at", payload.get("createdAt", utc_now_iso())
            ),
            updated_at=payload.get(
                "updated_at", payload.get("updatedAt", utc_now_iso())
            ),
        )

    def to_state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_web_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "venue": self.venue,
            "track": self.track,
            "method": self.method,
            "mu": round(self.mu, 3),
            "sigma": round(self.sigma, 3),
            "elo": int(self.elo),
            "matchesPlayed": int(self.matches_played),
            "reviewed": self.source == "human",
            "year": int(self.year),
            "paperUrl": self.paper_url,
            "status": self.status,
            "advisorPasses": self.advisor_passes,
            "advisorTotal": self.advisor_total,
            "advisorScore": round(self.advisor_score, 2),
            "reviewerScore": round(self.reviewer_score, 2),
            "reviewRecommendation": self.review_recommendation,
            "integrityFlags": self.integrity_flags,
        }


@dataclass
class MatchRecord:
    paper_a: str
    paper_b: str
    winner: str
    date: str
    judge_model: str
    swapped_consistent: bool
    rationale_short: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MatchRecord":
        return cls(
            paper_a=payload.get("paper_a", payload.get("paperA", "")),
            paper_b=payload.get("paper_b", payload.get("paperB", "")),
            winner=payload.get("winner", "tie"),
            date=payload.get("date", utc_now_iso()),
            judge_model=payload.get(
                "judge_model", payload.get("judgeModel", "unknown")
            ),
            swapped_consistent=bool(
                payload.get(
                    "swapped_consistent", payload.get("swappedConsistent", True)
                )
            ),
            rationale_short=payload.get(
                "rationale_short", payload.get("rationaleShort", "")
            ),
        )

    def to_state_dict(self) -> dict[str, Any]:
        return {
            "paper_a": self.paper_a,
            "paper_b": self.paper_b,
            "winner": self.winner,
            "date": self.date,
            "judge_model": self.judge_model,
            "swapped_consistent": self.swapped_consistent,
            "rationale_short": self.rationale_short,
        }

    def to_web_dict(self) -> dict[str, Any]:
        return {
            "paperA": self.paper_a,
            "paperB": self.paper_b,
            "winner": self.winner,
            "date": self.date,
        }
