# EPI-APE Backend Pipeline

This backend implements an end-to-end workflow inspired by Project APE and adapted for epidemiology:

1. `discovery`: find benchmark human papers and AI research candidates
2. `generation`: create reproducible AI paper workspaces
3. `advisors`: multi-model fatal-error checks (pass threshold)
4. `reviewers`: journal-style scoring and recommendation
5. `tournament`: pairwise judging with position swap and TrueSkill updates
6. `publish`: sync website data (`data/papers.json`, `data/matches.json`)
7. `github sync`: commit and push artifacts to remote

## Directory layout

- `backend/epi_ape/`: pipeline code
- `backend/state/`: persistent run state (papers, matches, settings snapshots)
- `papers/`: generated paper artifacts and replication materials

## Quick start

From repository root:

```bash
python -m backend.epi_ape.cli init
python -m backend.epi_ape.cli skills-audit
python -m backend.epi_ape.cli run-cycle --generate 3 --matches 20
# with git sync in same run (artifacts only: backend/state, data, papers):
python -m backend.epi_ape.cli run-cycle --generate 3 --matches 20 --sync-github --commit-message "chore: run epi-ape cycle"
```

This will update:

- `backend/state/papers.json`
- `backend/state/matches.json`
- `data/papers.json`
- `data/matches.json`

## Environment variables

- `EPI_APE_JUDGE_MODEL` (default `gemini-2.5-flash`)
- `EPI_APE_GENERATOR_MODEL` (default `claude-sonnet-4.5`)
- `EPI_APE_ADVISOR_MODELS` (comma list)
- `EPI_APE_REVIEWER_MODELS` (comma list)
- `EPI_APE_GITHUB_REMOTE` (default `origin`)
- `EPI_APE_GITHUB_BRANCH` (default current branch)

Optional keys for real model integration:

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `GOOGLE_API_KEY_FALLBACK` (used automatically if primary Gemini key fails)
- `XAI_API_KEY` (or `GROK_API_KEY`)
- `GITHUB_MODELS_TOKEN` (or `GITHUB_TOKEN`, for GitHub Models API)
- `DEEPSEEK_API_KEY`

If keys are missing, pipeline still runs in deterministic simulation mode for testing.
This means GitHub secrets are optional if you run the cycle locally and push from local.

Model strings can be prefixed by provider for explicit routing:

- `openai:gpt-5` or `openai:gpt-4.1`
- `gemini:gemini-2.5-flash`
- `xai:grok-4-fast`
- `github:openai/gpt-4.1`
- `deepseek:deepseek-chat`

Without prefix, routing is inferred from model name (`gpt*`, `gemini*`, `grok*`).

Important note on Copilot login: interactive Copilot web/editor login is not callable from this backend.
Use API credentials (OpenAI / Gemini / xAI / GitHub Models token) for automated advisor/reviewer/tournament calls.

Quick setup:

1. Copy `.env.example` to `.env.local`
2. Fill your keys
3. Run CLI commands normally (the backend auto-loads `.env` / `.env.local`)

## GitHub sync

Dry run:

```bash
python -m backend.epi_ape.cli sync-github
```

Commit and push:

```bash
python -m backend.epi_ape.cli sync-github --push --message "chore: update epi-ape papers and ratings"
```

By default, sync commits only artifact paths:

- `backend/state`
- `data`
- `papers`

To include all modified files, add `--all-files`.

## Notes

- Human benchmark papers are fetched from OpenAlex when available, with local fallback.
- Tournament uses `TrueSkill` when installed, else falls back to Elo-like updates.
- Advisor pass rule defaults to `3 of 4`.
