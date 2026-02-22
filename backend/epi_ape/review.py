from __future__ import annotations

from pathlib import Path

from .llm import advisor_evaluate, reviewer_evaluate
from .models import PaperRecord, utc_now_iso
from .utils import seeded_random


def _paper_dir(root_dir: Path, paper: PaperRecord) -> Path:
    return root_dir / paper.paper_url


def integrity_flags(root_dir: Path, paper: PaperRecord) -> list[str]:
    flags: list[str] = []
    base = _paper_dir(root_dir, paper)

    if not base.exists():
        return ["missing-paper-directory"]

    needed = [
        base / "paper.md",
        base / "scripts" / "analysis.R",
        base / "data" / "DATA_MANIFEST.md",
    ]
    for required in needed:
        if not required.exists():
            flags.append(f"missing-{required.name.lower()}")

    manifest = base / "data" / "DATA_MANIFEST.md"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8").lower()
        if "todo" in text:
            flags.append("data-manifest-incomplete")

    script = base / "scripts" / "analysis.R"
    if script.exists():
        text = script.read_text(encoding="utf-8").lower()
        if "rnorm(" in text:
            flags.append("uses-simulated-placeholder-data")

    return flags


def _paper_excerpt(root_dir: Path, paper: PaperRecord, limit: int = 2200) -> str:
    base = _paper_dir(root_dir, paper)
    paper_md = base / "paper.md"
    if not paper_md.exists():
        return ""

    text = paper_md.read_text(encoding="utf-8", errors="replace")
    return text[:limit]


def _advisor_pass_score(
    model_name: str,
    paper: PaperRecord,
    excerpt: str,
) -> tuple[bool, float]:
    llm_result = advisor_evaluate(
        model_name=model_name,
        paper_title=paper.title,
        paper_track=paper.track,
        paper_method=paper.method,
        integrity_flags=paper.integrity_flags,
        paper_excerpt=excerpt,
    )
    if llm_result is not None:
        return llm_result.passed, llm_result.score

    rnd = seeded_random(f"advisor:{model_name}:{paper.id}:{paper.title}")
    base = 66.0 + rnd.random() * 30.0

    penalties = 0.0
    if "placeholder" in paper.title.lower():
        penalties += 12.0
    if paper.integrity_flags:
        penalties += min(10.0, 2.0 * len(paper.integrity_flags))

    score = max(0.0, min(100.0, base - penalties))
    passed = score >= 66.0
    return passed, score


def run_advisor_stage(
    root_dir: Path,
    papers: list[PaperRecord],
    advisor_models: tuple[str, ...],
    required_passes: int = 3,
) -> list[PaperRecord]:
    touched: list[PaperRecord] = []

    for paper in papers:
        if paper.source != "ai" or paper.status not in {
            "draft",
            "advisor_failed",
            "idea",
        }:
            continue
        if paper.status == "idea":
            continue

        paper.integrity_flags = integrity_flags(root_dir, paper)
        excerpt = _paper_excerpt(root_dir, paper)

        passes = 0
        scores = []
        for model in advisor_models:
            passed, score = _advisor_pass_score(model, paper, excerpt)
            scores.append(score)
            if passed:
                passes += 1

        paper.advisor_total = len(advisor_models)
        paper.advisor_passes = passes
        paper.advisor_score = sum(scores) / len(scores) if scores else 0.0

        if passes >= required_passes:
            paper.status = "advisor_passed"
        else:
            paper.status = "advisor_failed"

        paper.updated_at = utc_now_iso()
        touched.append(paper)

    return touched


def _recommendation_from_score(score: float) -> str:
    if score >= 88.0:
        return "accept"
    if score >= 78.0:
        return "minor"
    if score >= 68.0:
        return "major"
    if score >= 58.0:
        return "r_and_r"
    return "reject"


def run_reviewer_stage(
    root_dir: Path,
    papers: list[PaperRecord],
    reviewer_models: tuple[str, ...],
) -> list[PaperRecord]:
    touched: list[PaperRecord] = []

    for paper in papers:
        if paper.source != "ai" or paper.status != "advisor_passed":
            continue

        excerpt = _paper_excerpt(root_dir, paper)
        base = seeded_random(f"reviewer-base:{paper.id}").random()
        score_values = []
        recommendations = []

        for model in reviewer_models:
            llm_result = reviewer_evaluate(
                model_name=model,
                paper_title=paper.title,
                paper_track=paper.track,
                paper_method=paper.method,
                integrity_flags=paper.integrity_flags,
                paper_excerpt=excerpt,
            )
            if llm_result is not None:
                score_values.append(llm_result.score)
                recommendations.append(llm_result.recommendation)
                continue

            rnd = seeded_random(f"reviewer:{model}:{paper.id}:{paper.title}")
            model_score = 60.0 + 35.0 * ((base + rnd.random()) / 2)
            model_score -= min(12.0, 2.5 * len(paper.integrity_flags))
            model_score = max(0.0, min(100.0, model_score))
            score_values.append(model_score)
            recommendations.append(_recommendation_from_score(model_score))

        overall = sum(score_values) / max(1, len(score_values))
        overall = max(0.0, min(100.0, overall))

        rec_counts: dict[str, int] = {}
        for rec in recommendations:
            rec_counts[rec] = rec_counts.get(rec, 0) + 1
        if rec_counts:
            selected_rec = sorted(
                rec_counts.items(),
                key=lambda item: (item[1], item[0]),
                reverse=True,
            )[0][0]
        else:
            selected_rec = _recommendation_from_score(overall)

        paper.reviewer_score = overall
        paper.review_recommendation = selected_rec
        paper.status = "reviewed"
        paper.updated_at = utc_now_iso()
        touched.append(paper)

    return touched
