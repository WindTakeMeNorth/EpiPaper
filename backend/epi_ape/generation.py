from __future__ import annotations

import json
from pathlib import Path

from .models import PaperRecord, utc_now_iso
from .utils import ensure_dir


def _paper_numeric_id(paper_id: str) -> int:
    tail = paper_id.split("_")[-1]
    return int(tail) if tail.isdigit() else 0


def _next_version_dir(papers_root: Path, paper_id: str) -> tuple[Path, int]:
    paper_root = papers_root / paper_id
    ensure_dir(paper_root)

    versions = []
    for entry in paper_root.iterdir():
        if not entry.is_dir() or not entry.name.startswith("v"):
            continue
        suffix = entry.name[1:]
        if suffix.isdigit():
            versions.append(int(suffix))

    nxt = max(versions, default=0) + 1
    version_dir = paper_root / f"v{nxt}"
    ensure_dir(version_dir)
    return version_dir, nxt


def _starter_paper_markdown(paper: PaperRecord, version: int) -> str:
    return f"""# {paper.title}

## Metadata

- Paper ID: `{paper.id}`
- Version: `v{version}`
- Track: `{paper.track}`
- Method: `{paper.method}`
- Generated at: `{utc_now_iso()}`

## Abstract (Draft)

This draft paper evaluates a policy intervention in an epidemiology context using a quasi-experimental design.
The current version is machine-generated and should be treated as a pre-review working draft.

## Policy Question

How does the intervention affect the selected health outcome, and through which equity channels are effects distributed?

## Identification Strategy

Primary design: **{paper.method}**.

Planned checks:

1. Event-time dynamics
2. Placebo or falsification tests
3. Heterogeneity by socioeconomic vulnerability
4. Sensitivity to alternative clustering levels

## Data Sources

- Public health surveillance source (to be finalized)
- Policy implementation registry (to be finalized)
- Geospatial and demographic covariates (to be finalized)

## Limitations (Preliminary)

- Potential measurement error in administrative coding.
- Potential spillovers across geographic boundaries.
- External validity may be limited outside observed settings.

## Reproducibility

Run analysis script:

```bash
Rscript scripts/analysis.R
```
"""


def _starter_analysis_r(paper: PaperRecord) -> str:
    return f"""# {paper.id} - {paper.title}
# Auto-generated starter script for EPI-APE.

suppressPackageStartupMessages({{
  library(data.table)
  library(fixest)
  library(ggplot2)
}})

cat("Running analysis for {paper.id}\\n")

# TODO: Replace with real data extraction code.
dt <- data.table(
  unit = rep(1:200, each = 8),
  year = rep(2018:2025, times = 200),
  treated = rep(sample(c(0, 1), 200, replace = TRUE), each = 8)
)

dt[, post := as.integer(year >= 2022)]
dt[, y := 0.5 * treated * post + rnorm(.N)]

mod <- feols(y ~ treated * post | unit + year, data = dt, vcov = ~unit)
print(summary(mod))

out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
fwrite(data.table(term = names(coef(mod)), estimate = as.numeric(coef(mod))), file.path(out_dir, "main_estimates.csv"))

png(file.path(out_dir, "event_plot.png"), width = 800, height = 500)
plot(dt$year, dt$y, pch = 19, col = rgb(0, 0, 0, 0.15), main = "Placeholder outcome path")
dev.off()

cat("Done. Outputs in ./outputs\\n")
"""


def _data_manifest() -> str:
    return """# Data manifest

List each input dataset before publication:

| Name | Source URL | Access date | License | Notes |
|------|------------|-------------|---------|-------|
| TODO | TODO | TODO | TODO | TODO |
"""


def _integrity_yaml() -> str:
    return """checks:
  - name: no-fabricated-data
    status: pending
  - name: reproducible-run
    status: pending
  - name: placebo-tests
    status: pending
"""


def generate_one(papers_root: Path, paper: PaperRecord) -> None:
    version_dir, version = _next_version_dir(papers_root, paper.id)
    scripts_dir = version_dir / "scripts"
    data_dir = version_dir / "data"
    outputs_dir = version_dir / "outputs"

    ensure_dir(scripts_dir)
    ensure_dir(data_dir)
    ensure_dir(outputs_dir)

    (version_dir / "paper.md").write_text(
        _starter_paper_markdown(paper, version),
        encoding="utf-8",
    )
    (scripts_dir / "analysis.R").write_text(
        _starter_analysis_r(paper), encoding="utf-8"
    )
    (data_dir / "DATA_MANIFEST.md").write_text(_data_manifest(), encoding="utf-8")
    (version_dir / "integrity.yml").write_text(_integrity_yaml(), encoding="utf-8")

    metadata = {
        "paper_id": paper.id,
        "version": version,
        "track": paper.track,
        "method": paper.method,
        "status": "draft",
        "created_at": utc_now_iso(),
    }
    (version_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    paper.venue = f"EPI-APE Working Paper #{_paper_numeric_id(paper.id)} (v{version})"
    paper.paper_url = str(version_dir.relative_to(papers_root.parent)).replace(
        "\\", "/"
    )
    paper.status = "draft"
    paper.updated_at = utc_now_iso()


def generate_batch(
    papers_root: Path, papers: list[PaperRecord], max_count: int
) -> list[PaperRecord]:
    candidates = [
        paper for paper in papers if paper.source == "ai" and paper.status == "idea"
    ]
    selected = candidates[:max_count]

    for paper in selected:
        generate_one(papers_root, paper)

    return selected
