from __future__ import annotations

from pathlib import Path


EPI_REQUIRED_SKILLS = [
    "pubmed-database",
    "openalex-database",
    "clinicaltrials-database",
    "geopandas",
    "statsmodels",
    "statistical-analysis",
    "scikit-learn",
    "pymc",
    "literature-review",
    "peer-review",
    "scientific-writing",
    "citation-management",
    "research-lookup",
    "hypothesis-generation",
    "scientific-critical-thinking",
    "exploratory-data-analysis",
]


def skills_dir(root_dir: Path) -> Path:
    return root_dir / ".codex" / "skills"


def audit_skills(root_dir: Path) -> dict[str, list[str]]:
    target = skills_dir(root_dir)
    installed = set()
    if target.exists():
        installed = {entry.name for entry in target.iterdir() if entry.is_dir()}

    required = set(EPI_REQUIRED_SKILLS)
    missing = sorted(required - installed)
    present = sorted(required & installed)

    return {
        "skills_dir": [str(target)],
        "present": present,
        "missing": missing,
    }
