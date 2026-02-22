from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root_dir: Path
    state_dir: Path
    papers_dir: Path
    web_data_dir: Path

    generator_model: str
    judge_model: str
    advisor_models: tuple[str, ...]
    reviewer_models: tuple[str, ...]

    github_remote: str
    github_branch: str


def _csv(name: str, default: str) -> tuple[str, ...]:
    raw = os.getenv(name, default)
    items = [part.strip() for part in raw.split(",")]
    return tuple(part for part in items if part)


def load_settings(root_dir: Path) -> Settings:
    state_dir = root_dir / "backend" / "state"
    papers_dir = root_dir / "papers"
    web_data_dir = root_dir / "data"

    return Settings(
        root_dir=root_dir,
        state_dir=state_dir,
        papers_dir=papers_dir,
        web_data_dir=web_data_dir,
        generator_model=os.getenv("EPI_APE_GENERATOR_MODEL", "claude-sonnet-4.5"),
        judge_model=os.getenv("EPI_APE_JUDGE_MODEL", "gemini-2.5-flash"),
        advisor_models=_csv(
            "EPI_APE_ADVISOR_MODELS",
            "openai:gpt-4.1,gemini:gemini-2.5-flash,xai:grok-4-fast,github:openai/gpt-4.1-mini",
        ),
        reviewer_models=_csv(
            "EPI_APE_REVIEWER_MODELS",
            "openai:gpt-4.1,gemini:gemini-2.5-flash,xai:grok-4-fast",
        ),
        github_remote=os.getenv("EPI_APE_GITHUB_REMOTE", "origin"),
        github_branch=os.getenv("EPI_APE_GITHUB_BRANCH", ""),
    )
