from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_settings
from .github_sync import sync_to_github
from .pipeline import publish_only, run_cycle
from .skills import audit_skills
from .utils import ensure_dir


def _root_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_env_files(root: Path) -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return

    for name in (".env", ".env.local"):
        env_file = root / name
        if env_file.exists():
            load_dotenv(env_file, override=False)


def cmd_init() -> int:
    root = _root_dir()
    _load_env_files(root)
    settings = load_settings(root)

    ensure_dir(settings.state_dir)
    ensure_dir(settings.papers_dir)
    ensure_dir(settings.web_data_dir)

    print(f"Initialized state dir: {settings.state_dir}")
    print(f"Initialized papers dir: {settings.papers_dir}")
    print(f"Web data dir: {settings.web_data_dir}")
    return 0


def cmd_skills_audit() -> int:
    root = _root_dir()
    report = audit_skills(root)

    print(f"Skills directory: {report['skills_dir'][0]}")
    print(f"Present ({len(report['present'])}):")
    for item in report["present"]:
        print(f"  - {item}")

    if report["missing"]:
        print(f"Missing ({len(report['missing'])}):")
        for item in report["missing"]:
            print(f"  - {item}")
        return 1

    print("All required EPI skills are installed.")
    return 0


def cmd_run_cycle(
    generate: int,
    matches: int,
    sync_github_after: bool,
    commit_message: str,
) -> int:
    root = _root_dir()
    _load_env_files(root)
    settings = load_settings(root)
    report = run_cycle(settings, generate_count=generate, match_count=matches)

    print("Cycle complete")
    print(f"- loaded papers: {report.loaded_papers}")
    print(f"- added human benchmarks: {report.added_human_benchmarks}")
    print(f"- added ai ideas: {report.added_ai_ideas}")
    print(f"- generated ai papers: {report.generated_ai_papers}")
    print(f"- advisor-reviewed papers: {report.advisor_touched}")
    print(f"- reviewer-reviewed papers: {report.reviewer_touched}")
    print(f"- new matches: {report.new_matches}")

    if sync_github_after:
        print("Running GitHub sync...")
        result = sync_to_github(
            root_dir=root,
            remote=settings.github_remote,
            branch=settings.github_branch,
            push=True,
            commit_message=commit_message,
        )
        print(result.message)
        for line in result.details:
            if line:
                print(line)
        if not result.ok:
            return 1

    return 0


def cmd_publish() -> int:
    root = _root_dir()
    _load_env_files(root)
    settings = load_settings(root)
    publish_only(settings)
    print("Published web data to data/papers.json and data/matches.json")
    return 0


def cmd_sync_github(push: bool, message: str) -> int:
    root = _root_dir()
    _load_env_files(root)
    settings = load_settings(root)

    result = sync_to_github(
        root_dir=root,
        remote=settings.github_remote,
        branch=settings.github_branch,
        push=push,
        commit_message=message,
    )

    print(result.message)
    for line in result.details:
        if line:
            print(line)

    return 0 if result.ok else 1


def main() -> int:
    root = _root_dir()
    _load_env_files(root)

    parser = argparse.ArgumentParser(description="EPI-APE backend CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize directories")
    sub.add_parser("skills-audit", help="Verify required EPI skills")

    run_parser = sub.add_parser("run-cycle", help="Run full pipeline cycle")
    run_parser.add_argument(
        "--generate", type=int, default=3, help="Number of new AI papers to generate"
    )
    run_parser.add_argument(
        "--matches", type=int, default=20, help="Number of tournament matches"
    )
    run_parser.add_argument(
        "--sync-github",
        action="store_true",
        help="Commit and push after cycle completes",
    )
    run_parser.add_argument(
        "--commit-message",
        default="chore: run epi-ape cycle",
        help="Commit message when --sync-github is enabled",
    )

    sub.add_parser("publish-web", help="Publish current state into web data files")

    sync_parser = sub.add_parser(
        "sync-github", help="Commit and optionally push changes"
    )
    sync_parser.add_argument(
        "--push", action="store_true", help="Commit and push changes"
    )
    sync_parser.add_argument(
        "--message",
        default="chore: sync epi-ape papers and tournament state",
        help="Commit message when --push is provided",
    )

    args = parser.parse_args()

    if args.command == "init":
        return cmd_init()
    if args.command == "skills-audit":
        return cmd_skills_audit()
    if args.command == "run-cycle":
        return cmd_run_cycle(
            generate=args.generate,
            matches=args.matches,
            sync_github_after=args.sync_github,
            commit_message=args.commit_message,
        )
    if args.command == "publish-web":
        return cmd_publish()
    if args.command == "sync-github":
        return cmd_sync_github(push=args.push, message=args.message)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
