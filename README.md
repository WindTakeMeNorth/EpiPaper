# EPI-APE

EPI-APE is an epidemiology-focused adaptation of the APE workflow.

It includes:

- A public-facing leaderboard website (`index.html`, `methodology.html`, `agendas.html`, `about.html`)
- A backend pipeline that automates paper discovery, AI generation scaffolding, advisor/reviewer scoring, tournament updates, and website sync

Core tracks:

- Social & Spatial Epidemiology
- Community Health
- Environmental EPI
- Infectious Disease Dynamics
- Health Equity & Policy

## Website

- `index.html`: leaderboard, stats, filters, recent matches
- `methodology.html`: process and integrity checks
- `agendas.html`: research tracks
- `about.html`: project scope and caveats
- `assets/css/styles.css`: full style system
- `assets/js/app.js`: frontend rendering logic

Run locally:

```bash
python -m http.server 4173
```

Then open `http://localhost:4173`.

## Backend pipeline

Backend code lives in `backend/epi_ape`.

High-level flow:

1. Discover benchmark human papers and AI candidate ideas
2. Generate reproducible AI paper workspaces under `papers/`
3. Run advisor stage (multi-model fatal error checks)
4. Run reviewer stage (journal-style scoring and recommendation)
5. Run position-swapped tournament and update ratings
6. Publish synced data to `data/papers.json` and `data/matches.json`
7. Optional GitHub commit/push sync

Initialize and run a cycle:

```bash
python -m backend.epi_ape.cli init
python -m backend.epi_ape.cli run-cycle --generate 3 --matches 20
```

Automated daily run is configured in `.github/workflows/epi-ape-cycle.yml`.

## Skills installation

Installed source repo:

- `claude-scientific-skills/`

Installed project-level skills:

- `.codex/skills/pubmed-database`
- `.codex/skills/openalex-database`
- `.codex/skills/clinicaltrials-database`
- `.codex/skills/geopandas`
- `.codex/skills/statsmodels`
- `.codex/skills/statistical-analysis`
- `.codex/skills/scikit-learn`
- `.codex/skills/pymc`
- `.codex/skills/literature-review`
- `.codex/skills/peer-review`
- `.codex/skills/scientific-writing`
- `.codex/skills/citation-management`
- `.codex/skills/research-lookup`
- `.codex/skills/hypothesis-generation`
- `.codex/skills/scientific-critical-thinking`
- `.codex/skills/exploratory-data-analysis`
- `.codex/skills/pydeseq2`

Audit required skills:

```bash
python -m backend.epi_ape.cli skills-audit
```

## Data model (website)

`data/papers.json` includes:

- identity: `id`, `title`, `source`, `venue`, `track`, `method`, `year`, `paperUrl`
- rating: `mu`, `sigma`, `elo`, `matchesPlayed`
- review: `advisorPasses`, `advisorTotal`, `advisorScore`, `reviewerScore`, `reviewRecommendation`, `integrityFlags`

`data/matches.json` includes:

- aggregate stats: `totalMatches`, `aiVsHuman`, `lastUpdated`
- `recentMatches` list for the homepage
