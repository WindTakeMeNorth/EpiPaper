from __future__ import annotations

from itertools import cycle

from .models import PaperRecord, utc_now_iso
from .utils import get_json, seeded_random


TRACKS = [
    "Social & Spatial EPI",
    "Community Health",
    "Environmental EPI",
    "Infectious Disease Dynamics",
    "Health Equity & Policy",
]


METHODS = [
    "Difference-in-Differences",
    "Event Study",
    "Regression Discontinuity",
    "Synthetic Control",
    "Spatial Panel Model",
    "Target Trial Emulation",
    "Interrupted Time Series",
]


def infer_track(title: str) -> str:
    text = title.lower()
    if any(
        token in text
        for token in ["spatial", "neighborhood", "district", "geograph", "commut"]
    ):
        return "Social & Spatial EPI"
    if any(
        token in text for token in ["community", "primary care", "clinic", "worker"]
    ):
        return "Community Health"
    if any(
        token in text
        for token in ["air", "heat", "pollution", "climate", "flood", "temperature"]
    ):
        return "Environmental EPI"
    if any(
        token in text
        for token in [
            "outbreak",
            "vaccine",
            "transmission",
            "influenza",
            "covid",
            "rsv",
        ]
    ):
        return "Infectious Disease Dynamics"
    return "Health Equity & Policy"


def infer_method(title: str) -> str:
    rnd = seeded_random(title)
    return METHODS[rnd.randrange(len(METHODS))]


def _next_id(existing: list[PaperRecord], prefix: str) -> str:
    values = []
    for paper in existing:
        if paper.id.startswith(prefix):
            tail = paper.id.split("_")[-1]
            if tail.isdigit():
                values.append(int(tail))

    nxt = max(values, default=0) + 1
    return f"{prefix}_{nxt:04d}"


def _fetch_openalex_benchmarks(limit: int = 20) -> list[dict]:
    queries = [
        "epidemiology policy evaluation",
        "community health intervention",
        "spatial epidemiology health inequality",
    ]

    items: list[dict] = []
    seen_titles: set[str] = set()

    for query in queries:
        payload = get_json(
            "https://api.openalex.org/works",
            {
                "search": query,
                "filter": "type:article,is_retracted:false,from_publication_date:2019-01-01",
                "per-page": "15",
                "sort": "cited_by_count:desc",
            },
        )

        for work in payload.get("results", []):
            title = (work.get("title") or "").strip()
            if not title:
                continue

            key = title.casefold()
            if key in seen_titles:
                continue

            seen_titles.add(key)
            items.append(work)
            if len(items) >= limit:
                return items

    return items


def _fallback_human_papers() -> list[dict]:
    return [
        {
            "title": "Heat Action Plans and Urban Mortality: A Multi-City Comparative Study",
            "venue": "International Journal of Epidemiology",
            "year": 2023,
        },
        {
            "title": "Community Health Workers and Maternal Care Continuity in Underserved Regions",
            "venue": "Lancet Public Health",
            "year": 2024,
        },
        {
            "title": "Neighborhood Segregation and Cardiovascular Risk in Older Adults",
            "venue": "Epidemiology",
            "year": 2022,
        },
        {
            "title": "School Ventilation Standards and Seasonal Respiratory Transmission",
            "venue": "American Journal of Epidemiology",
            "year": 2023,
        },
        {
            "title": "Flood Mitigation Policy and Enteric Disease Incidence",
            "venue": "BMJ Global Health",
            "year": 2021,
        },
    ]


def discover_human_benchmarks(
    existing: list[PaperRecord], target_additions: int = 6
) -> list[PaperRecord]:
    current = [paper for paper in existing if paper.source == "human"]
    if len(current) >= target_additions:
        return []

    to_add = target_additions - len(current)
    found: list[dict] = []

    try:
        openalex_items = _fetch_openalex_benchmarks(limit=max(10, to_add * 2))
        for work in openalex_items:
            venue = (
                work.get("primary_location", {})
                .get("source", {})
                .get("display_name", "Unknown Venue")
            )
            found.append(
                {
                    "title": work.get("title") or "Untitled",
                    "venue": venue,
                    "year": int(work.get("publication_year") or 2024),
                }
            )
    except Exception:
        found = _fallback_human_papers()

    if not found:
        found = _fallback_human_papers()

    rng = seeded_random("human-benchmark")
    score_base = cycle([34.0, 33.4, 32.7, 31.9, 31.2, 30.8, 30.1])

    title_seen = {paper.title.casefold() for paper in existing}
    additions: list[PaperRecord] = []

    for raw in found:
        if len(additions) >= to_add:
            break

        title = raw["title"].strip()
        if not title:
            continue
        if title.casefold() in title_seen:
            continue

        title_seen.add(title.casefold())

        mu = next(score_base) + rng.uniform(-0.6, 0.6)
        sigma = rng.uniform(0.9, 1.4)
        elo = int(1500 + (mu - 25.0) * 32)

        additions.append(
            PaperRecord(
                id=_next_id(existing + additions, "epi_h"),
                title=title,
                source="human",
                venue=raw["venue"],
                track=infer_track(title),
                method=infer_method(title),
                year=int(raw.get("year", 2024)),
                paper_url="#",
                status="peer_reviewed",
                mu=mu,
                sigma=sigma,
                elo=elo,
                advisor_passes=4,
                advisor_total=4,
                advisor_score=95.0,
                reviewer_score=92.0,
                review_recommendation="accept",
                created_at=utc_now_iso(),
                updated_at=utc_now_iso(),
            )
        )

    return additions


def propose_ai_ideas(existing: list[PaperRecord], count: int = 5) -> list[PaperRecord]:
    interventions = [
        "heat alert policy",
        "community clinic weekend opening",
        "bus fare subsidy for outpatient follow-up",
        "mobile vaccine campaign",
        "clean cooking transition",
        "school air filtration mandate",
        "housing retrofit program",
        "water chlorination enforcement",
        "telehealth parity expansion",
        "community pharmacy hypertension bundle",
    ]

    outcomes = [
        "respiratory hospitalization",
        "diabetes continuity of care",
        "maternal visit completion",
        "outbreak response delay",
        "preventive screening uptake",
        "heatstroke mortality",
        "emergency department congestion",
        "vaccine booster equity",
    ]

    geos = [
        "urban districts",
        "rural counties",
        "border municipalities",
        "low-income neighborhoods",
        "informal settlements",
    ]

    methods = METHODS
    track_cycle = cycle(TRACKS)
    rnd = seeded_random("ai-idea-proposals")

    existing_titles = {paper.title.casefold() for paper in existing}
    additions: list[PaperRecord] = []
    attempts = 0

    while len(additions) < count and attempts < 200:
        attempts += 1
        intervention = rnd.choice(interventions)
        outcome = rnd.choice(outcomes)
        geography = rnd.choice(geos)
        track = next(track_cycle)
        method = rnd.choice(methods)
        title = f"{intervention.title()} and {outcome.title()} in {geography.title()}"

        key = title.casefold()
        if key in existing_titles:
            continue

        existing_titles.add(key)
        additions.append(
            PaperRecord(
                id=_next_id(existing + additions, "epi_a"),
                title=title,
                source="ai",
                venue="EPI-APE Candidate",
                track=track,
                method=method,
                year=2026,
                paper_url="#",
                status="idea",
                mu=25.0,
                sigma=8.333,
                elo=1500,
                contributor="generator",
                created_at=utc_now_iso(),
                updated_at=utc_now_iso(),
            )
        )

    return additions
