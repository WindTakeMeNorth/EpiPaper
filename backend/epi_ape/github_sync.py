from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitSyncResult:
    ok: bool
    message: str
    details: list[str]


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def sync_to_github(
    root_dir: Path,
    remote: str,
    branch: str,
    push: bool,
    commit_message: str,
) -> GitSyncResult:
    details: list[str] = []

    probe = _run_git(["rev-parse", "--is-inside-work-tree"], root_dir)
    if probe.returncode != 0:
        return GitSyncResult(
            ok=False,
            message="Not a git repository. Initialize git before sync.",
            details=[probe.stderr.strip() or probe.stdout.strip()],
        )

    status = _run_git(["status", "--short"], root_dir)
    if status.returncode != 0:
        return GitSyncResult(
            ok=False, message="git status failed.", details=[status.stderr.strip()]
        )

    if not status.stdout.strip():
        return GitSyncResult(ok=True, message="No changes to sync.", details=[])

    details.append(status.stdout.strip())

    if not push:
        return GitSyncResult(
            ok=True,
            message="Dry run only. Re-run with --push to commit and push.",
            details=details,
        )

    add = _run_git(["add", "."], root_dir)
    if add.returncode != 0:
        return GitSyncResult(
            ok=False, message="git add failed.", details=[add.stderr.strip()]
        )

    commit = _run_git(["commit", "-m", commit_message], root_dir)
    if commit.returncode != 0:
        if (
            "nothing to commit" in commit.stdout.lower()
            or "nothing to commit" in commit.stderr.lower()
        ):
            return GitSyncResult(ok=True, message="No changes to commit.", details=[])
        return GitSyncResult(
            ok=False,
            message="git commit failed.",
            details=[commit.stderr.strip(), commit.stdout.strip()],
        )

    details.append(commit.stdout.strip())

    if not branch:
        branch_proc = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], root_dir)
        if branch_proc.returncode == 0:
            branch = branch_proc.stdout.strip()

    push_proc = _run_git(["push", "-u", remote, branch], root_dir)
    if push_proc.returncode != 0:
        return GitSyncResult(
            ok=False,
            message="Commit succeeded but push failed.",
            details=[push_proc.stderr.strip(), push_proc.stdout.strip()],
        )

    details.append(push_proc.stdout.strip())
    return GitSyncResult(
        ok=True, message="Changes committed and pushed.", details=details
    )
