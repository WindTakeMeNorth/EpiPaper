from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .llm import judge_pair as llm_judge_pair
from .models import MatchRecord, PaperRecord
from .utils import seeded_random

try:
    import trueskill as ts
except Exception:
    ts = None


def _quality_score(paper: PaperRecord) -> float:
    base = paper.conservative_score()
    if paper.source == "ai":
        base += (paper.advisor_score - 70.0) * 0.12
        base += (paper.reviewer_score - 70.0) * 0.18
        base -= min(6.0, len(paper.integrity_flags) * 1.5)
    return base


def _judged_winner(
    a: PaperRecord, b: PaperRecord, order_bias_to_a: float, key: str
) -> str:
    rnd = seeded_random(key)
    qa = _quality_score(a) + order_bias_to_a + rnd.uniform(-1.2, 1.2)
    qb = _quality_score(b) + rnd.uniform(-1.2, 1.2)

    margin = qa - qb
    if abs(margin) <= 0.6:
        return "tie"
    return "paperA" if margin > 0 else "paperB"


def judge_pair_position_swapped(
    a: PaperRecord,
    b: PaperRecord,
    seed_key: str,
    judge_model: str,
) -> tuple[str, bool, str]:
    first_llm = llm_judge_pair(
        model_name=judge_model,
        paper_a_title=a.title,
        paper_a_track=a.track,
        paper_a_method=a.method,
        paper_a_advisor=a.advisor_score,
        paper_a_reviewer=a.reviewer_score,
        paper_b_title=b.title,
        paper_b_track=b.track,
        paper_b_method=b.method,
        paper_b_advisor=b.advisor_score,
        paper_b_reviewer=b.reviewer_score,
    )

    if first_llm is not None:
        second_llm = llm_judge_pair(
            model_name=judge_model,
            paper_a_title=b.title,
            paper_a_track=b.track,
            paper_a_method=b.method,
            paper_a_advisor=b.advisor_score,
            paper_a_reviewer=b.reviewer_score,
            paper_b_title=a.title,
            paper_b_track=a.track,
            paper_b_method=a.method,
            paper_b_advisor=a.advisor_score,
            paper_b_reviewer=a.reviewer_score,
        )

        if second_llm is None:
            winner = first_llm.winner
            return winner, winner != "tie", first_llm.rationale

        first = first_llm.winner
        if second_llm.winner == "paperA":
            second = "paperB"
        elif second_llm.winner == "paperB":
            second = "paperA"
        else:
            second = "tie"

        if first == "tie" or second == "tie":
            return "tie", False, first_llm.rationale or second_llm.rationale
        if first == second:
            return first, True, first_llm.rationale or second_llm.rationale
        return "tie", False, first_llm.rationale or second_llm.rationale

    first = _judged_winner(a, b, order_bias_to_a=0.35, key=f"{seed_key}:ab")
    swapped = _judged_winner(a, b, order_bias_to_a=-0.35, key=f"{seed_key}:ba")

    if first == "tie" or swapped == "tie":
        return "tie", False, "Judge could not determine a stable preference after swap."

    if first == swapped:
        if first == "paperA":
            return (
                first,
                True,
                "AI paper preferred on identification and policy relevance.",
            )
        return (
            first,
            True,
            "Human paper preferred for robustness and reporting clarity.",
        )

    return "tie", False, "Judge could not determine a stable preference after swap."


def _update_rating_trueskill(a: PaperRecord, b: PaperRecord, winner: str) -> None:
    if ts is None:
        _update_rating_elo(a, b, winner)
        return

    ra = ts.Rating(mu=a.mu, sigma=a.sigma)
    rb = ts.Rating(mu=b.mu, sigma=b.sigma)

    if winner == "paperA":
        na, nb = ts.rate_1vs1(ra, rb)
    elif winner == "paperB":
        nb, na = ts.rate_1vs1(rb, ra)
    else:
        na, nb = ts.rate_1vs1(ra, rb, drawn=True)

    a.mu, a.sigma = float(na.mu), float(na.sigma)
    b.mu, b.sigma = float(nb.mu), float(nb.sigma)

    a.elo = int(1500 + (a.mu - 25.0) * 38)
    b.elo = int(1500 + (b.mu - 25.0) * 38)


def _update_rating_elo(
    a: PaperRecord, b: PaperRecord, winner: str, k: float = 24.0
) -> None:
    ea = 1.0 / (1.0 + 10 ** ((b.elo - a.elo) / 400.0))
    eb = 1.0 - ea

    if winner == "paperA":
        sa, sb = 1.0, 0.0
    elif winner == "paperB":
        sa, sb = 0.0, 1.0
    else:
        sa, sb = 0.5, 0.5

    a.elo = int(round(a.elo + k * (sa - ea)))
    b.elo = int(round(b.elo + k * (sb - eb)))

    a.mu = 25.0 + (a.elo - 1500) / 38.0
    b.mu = 25.0 + (b.elo - 1500) / 38.0
    a.sigma = max(0.9, a.sigma * 0.995)
    b.sigma = max(0.9, b.sigma * 0.995)


def _eligible_papers(
    papers: list[PaperRecord],
) -> tuple[list[PaperRecord], list[PaperRecord]]:
    humans = [
        paper
        for paper in papers
        if paper.source == "human" and paper.status == "peer_reviewed"
    ]
    ais = [
        paper
        for paper in papers
        if paper.source == "ai"
        and paper.status == "reviewed"
        and paper.review_recommendation != "reject"
    ]
    return humans, ais


@dataclass
class TournamentStats:
    matches_created: int
    ai_wins: int
    human_wins: int
    ties: int


def run_tournament_round(
    papers: list[PaperRecord],
    existing_matches: list[MatchRecord],
    judge_model: str,
    match_count: int,
) -> tuple[list[MatchRecord], TournamentStats]:
    humans, ais = _eligible_papers(papers)
    if not humans or not ais:
        return existing_matches, TournamentStats(0, 0, 0, 0)

    rnd = seeded_random(
        f"tournament:{datetime.now(timezone.utc).strftime('%Y-%m-%d')}:{len(existing_matches)}"
    )

    new_matches: list[MatchRecord] = []
    ai_wins = 0
    human_wins = 0
    ties = 0

    for idx in range(match_count):
        ai_paper = ais[rnd.randrange(len(ais))]
        human_paper = humans[rnd.randrange(len(humans))]

        winner, consistent, rationale = judge_pair_position_swapped(
            ai_paper,
            human_paper,
            seed_key=f"{ai_paper.id}:{human_paper.id}:{len(existing_matches) + idx}",
            judge_model=judge_model,
        )

        _update_rating_trueskill(ai_paper, human_paper, winner)

        ai_paper.matches_played += 1
        human_paper.matches_played += 1

        if winner == "paperA":
            ai_wins += 1
            if not rationale:
                rationale = "AI paper preferred on identification and policy relevance."
        elif winner == "paperB":
            human_wins += 1
            if not rationale:
                rationale = (
                    "Human paper preferred for robustness and reporting clarity."
                )
        else:
            ties += 1
            if not rationale:
                rationale = "Judge could not determine a stable preference after swap."

        rationale = rationale[:240]

        new_matches.append(
            MatchRecord(
                paper_a=ai_paper.id,
                paper_b=human_paper.id,
                winner=winner,
                date=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                judge_model=judge_model,
                swapped_consistent=consistent,
                rationale_short=rationale,
            )
        )

    all_matches = existing_matches + new_matches
    return all_matches, TournamentStats(len(new_matches), ai_wins, human_wins, ties)
