# EPI-APE Pipeline Plan

This document mirrors the APE-style flow and adapts it for epidemiology.

## Stage 1 - Discovery

Inputs:

- Human benchmark papers from OpenAlex (and later PubMed / curated top journals)
- AI candidate questions generated in track-constrained templates

Outputs:

- `PaperRecord` entries with IDs, tracks, method tags, and baseline ratings

## Stage 2 - Generation

For each selected AI idea:

- Create `papers/<paper_id>/vN/`
- Generate draft manuscript (`paper.md`)
- Generate starter analysis (`scripts/analysis.R`)
- Add data manifest (`data/DATA_MANIFEST.md`)
- Add integrity checklist (`integrity.yml`)

## Stage 3 - Advisors (fatal error gate)

Default advisor ensemble:

- GPT-5.2
- Gemini 2.5 Flash
- Grok 4 Fast
- Codex Mini

Rule:

- At least `3/4` advisors must pass for reviewer stage.

Signals:

- Identification credibility
- Data integrity concerns
- Code and reproducibility sanity

## Stage 4 - Reviewers (journal-style scoring)

Default reviewer ensemble:

- GPT-5.2
- Gemini 2.5 Flash
- Grok 4 Fast

Outputs per paper:

- Reviewer score (0-100)
- Recommendation: `accept | minor | major | r_and_r | reject`

## Stage 5 - Tournament

Match mechanics:

- AI paper vs benchmark human paper
- Position-swapped judging to reduce order bias
- If outcomes disagree after swap, mark tie

Ratings:

- Update with TrueSkill when available
- Conservative rank: `mu - 3 * sigma`

## Stage 6 - Publish / Sync

Publish files:

- `data/papers.json`
- `data/matches.json`

Frontend displays:

- Advisor pass rate and score
- Reviewer score and recommendation
- Updated ratings and recent matches

## Stage 7 - GitHub synchronization

Pipeline supports:

- Dry-run status check (`sync-github`)
- Optional commit + push (`sync-github --push`)

This ensures generated papers, review metadata, and tournament state can be mirrored to GitHub.
