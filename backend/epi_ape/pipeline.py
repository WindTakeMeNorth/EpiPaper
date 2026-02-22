from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .discovery import discover_human_benchmarks, propose_ai_ideas
from .generation import generate_batch
from .models import MatchRecord, PaperRecord, utc_now_iso
from .publish import publish_web_data
from .review import run_advisor_stage, run_reviewer_stage
from .storage import StateStore
from .tournament import run_tournament_round
from .utils import load_json


@dataclass
class CycleReport:
    loaded_papers: int
    added_human_benchmarks: int
    added_ai_ideas: int
    generated_ai_papers: int
    advisor_touched: int
    reviewer_touched: int
    new_matches: int


def _bootstrap_papers_from_web_data(web_data_dir: Path) -> list[PaperRecord]:
    path = web_data_dir / "papers.json"
    raw = load_json(path, default=[])
    return [PaperRecord.from_dict(item) for item in raw]


def _bootstrap_matches_from_web_data(web_data_dir: Path) -> list[MatchRecord]:
    path = web_data_dir / "matches.json"
    raw = load_json(path, default={})
    items = raw.get("recentMatches", [])
    return [MatchRecord.from_dict(item) for item in items]


def _index_by_id(papers: list[PaperRecord]) -> dict[str, PaperRecord]:
    return {paper.id: paper for paper in papers}


def _normalize_papers(papers: list[PaperRecord]) -> None:
    for paper in papers:
        if paper.source == "human":
            paper.status = "peer_reviewed"
            if paper.advisor_total == 0:
                paper.advisor_total = 4
            if paper.advisor_passes == 0:
                paper.advisor_passes = paper.advisor_total
            if paper.advisor_score == 0.0:
                paper.advisor_score = 95.0
            if paper.reviewer_score == 0.0:
                paper.reviewer_score = 92.0
            if paper.review_recommendation in {"pending", ""}:
                paper.review_recommendation = "accept"
            if paper.sigma > 2.5:
                paper.sigma = 1.4
        elif paper.source == "ai":
            if paper.status == "peer_reviewed":
                paper.status = "reviewed"
            if paper.status == "":
                paper.status = "idea"


def run_cycle(
    settings: Settings,
    generate_count: int,
    match_count: int,
) -> CycleReport:
    store = StateStore(settings.state_dir)
    store.init_dirs()

    papers = store.load_papers()
    matches = store.load_matches()

    if not papers:
        papers = _bootstrap_papers_from_web_data(settings.web_data_dir)
    if not matches:
        matches = _bootstrap_matches_from_web_data(settings.web_data_dir)

    _normalize_papers(papers)

    initial_len = len(papers)

    human_additions = discover_human_benchmarks(papers, target_additions=8)
    papers.extend(human_additions)

    idea_pool = [
        paper for paper in papers if paper.source == "ai" and paper.status == "idea"
    ]
    need_ideas = max(0, generate_count - len(idea_pool))
    ai_ideas = propose_ai_ideas(papers, count=need_ideas)
    papers.extend(ai_ideas)

    generated = generate_batch(settings.papers_dir, papers, max_count=generate_count)

    advisor_touched = run_advisor_stage(
        settings.root_dir,
        papers,
        settings.advisor_models,
        required_passes=min(3, len(settings.advisor_models)),
    )
    reviewer_touched = run_reviewer_stage(
        settings.root_dir,
        papers,
        settings.reviewer_models,
    )

    matches, tournament_stats = run_tournament_round(
        papers,
        matches,
        judge_model=settings.judge_model,
        match_count=match_count,
    )

    by_id = _index_by_id(papers)
    for match in matches[-tournament_stats.matches_created :]:
        if match.paper_a in by_id:
            by_id[match.paper_a].updated_at = utc_now_iso()
        if match.paper_b in by_id:
            by_id[match.paper_b].updated_at = utc_now_iso()

    store.save_papers(papers)
    store.save_matches(matches)
    store.save_meta(
        {
            "last_cycle_at": utc_now_iso(),
            "total_papers": len(papers),
            "total_matches": len(matches),
            "generator_model": settings.generator_model,
            "judge_model": settings.judge_model,
            "advisor_models": list(settings.advisor_models),
            "reviewer_models": list(settings.reviewer_models),
        }
    )

    publish_web_data(settings.web_data_dir, papers, matches)

    return CycleReport(
        loaded_papers=initial_len,
        added_human_benchmarks=len(human_additions),
        added_ai_ideas=len(ai_ideas),
        generated_ai_papers=len(generated),
        advisor_touched=len(advisor_touched),
        reviewer_touched=len(reviewer_touched),
        new_matches=tournament_stats.matches_created,
    )


def publish_only(settings: Settings) -> None:
    store = StateStore(settings.state_dir)
    papers = store.load_papers()
    matches = store.load_matches()

    if not papers:
        papers = _bootstrap_papers_from_web_data(settings.web_data_dir)
    if not matches:
        matches = _bootstrap_matches_from_web_data(settings.web_data_dir)

    _normalize_papers(papers)

    publish_web_data(settings.web_data_dir, papers, matches)
