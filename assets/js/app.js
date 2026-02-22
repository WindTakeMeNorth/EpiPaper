const state = {
  papers: [],
  matches: null,
  filters: {
    source: "all",
    track: "all",
    search: "",
  },
};

const numberFmt = new Intl.NumberFormat("en-US");

const conservativeScore = (paper) => paper.mu - 3 * paper.sigma;

const sourceLabel = (source) => (source === "ai" ? "AI" : "Human");

const toDateLabel = (iso) => {
  if (!iso) return "-";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "-";

  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

function getTrackOptions(papers) {
  return [...new Set(papers.map((p) => p.track))].sort((a, b) =>
    a.localeCompare(b)
  );
}

function fillTrackFilter() {
  const trackFilter = document.querySelector("#filter-track");
  if (!trackFilter) return;

  const options = getTrackOptions(state.papers);
  for (const track of options) {
    const option = document.createElement("option");
    option.value = track;
    option.textContent = track;
    trackFilter.append(option);
  }
}

function rankLookup() {
  const sorted = [...state.papers].sort(
    (a, b) => conservativeScore(b) - conservativeScore(a)
  );

  const lookup = new Map();
  sorted.forEach((paper, index) => {
    lookup.set(paper.id, index + 1);
  });

  return lookup;
}

function filteredPapers() {
  const term = state.filters.search.trim().toLowerCase();

  return state.papers
    .filter((paper) => {
      if (state.filters.source !== "all" && paper.source !== state.filters.source) {
        return false;
      }

      if (state.filters.track !== "all" && paper.track !== state.filters.track) {
        return false;
      }

      if (!term) return true;

      const blob = `${paper.title} ${paper.method} ${paper.venue}`.toLowerCase();
      return blob.includes(term);
    })
    .sort((a, b) => conservativeScore(b) - conservativeScore(a));
}

function renderStats() {
  const totalPapersEl = document.querySelector("#stat-total-papers");
  const totalMatchesEl = document.querySelector("#stat-total-matches");
  const aiWinRateEl = document.querySelector("#stat-ai-win-rate");
  const updatedEl = document.querySelector("#stat-last-updated");

  if (!totalPapersEl || !totalMatchesEl || !aiWinRateEl || !updatedEl) return;

  const aiWins = state.matches?.aiVsHuman?.aiWins ?? 0;
  const humanWins = state.matches?.aiVsHuman?.humanWins ?? 0;
  const denominator = aiWins + humanWins;
  const aiRate = denominator > 0 ? (aiWins / denominator) * 100 : 0;

  totalPapersEl.textContent = numberFmt.format(state.papers.length);
  totalMatchesEl.textContent = numberFmt.format(state.matches?.totalMatches ?? 0);
  aiWinRateEl.textContent = `${clamp(aiRate, 0, 100).toFixed(1)}%`;
  updatedEl.textContent = toDateLabel(state.matches?.lastUpdated);
}

function renderTopAiPapers() {
  const mount = document.querySelector("#top-ai-list");
  if (!mount) return;

  const top = state.papers
    .filter((paper) => paper.source === "ai")
    .sort((a, b) => conservativeScore(b) - conservativeScore(a))
    .slice(0, 3);

  if (top.length === 0) {
    mount.innerHTML = '<p class="top-meta">No AI papers available yet.</p>';
    return;
  }

  mount.innerHTML = top
    .map((paper, index) => {
      const score = conservativeScore(paper).toFixed(1);
      return `
        <article class="top-item">
          <h3>#${index + 1} ${paper.title}</h3>
          <p class="top-meta">${paper.track} | ${paper.method} | Cons. ${score} | Elo ${paper.elo}</p>
        </article>
      `;
    })
    .join("");
}

function renderLeaderboard() {
  const body = document.querySelector("#leaderboard-body");
  if (!body) return;

  const rows = filteredPapers();
  const ranks = rankLookup();

  if (rows.length === 0) {
    body.innerHTML =
      '<tr><td colspan="12">No papers match your filter criteria.</td></tr>';
    return;
  }

  body.innerHTML = rows
    .map((paper) => {
      const rank = ranks.get(paper.id);
      const reviewed = paper.reviewed ? "Yes" : "No";
      const reviewedClass = paper.reviewed ? "status-yes" : "status-no";
      const score = conservativeScore(paper).toFixed(1);
      const advisorTotal = paper.advisorTotal ?? 0;
      const advisorPasses = paper.advisorPasses ?? 0;
      const advisorScore = paper.advisorScore ?? 0;
      const advisorText =
        advisorTotal > 0
          ? `${advisorPasses}/${advisorTotal} (${advisorScore.toFixed(0)})`
          : "-";
      const reviewerScore = paper.reviewerScore ?? 0;
      const reviewerRec = paper.reviewRecommendation ?? "n/a";
      const reviewerText =
        paper.source === "ai" ? `${reviewerScore.toFixed(0)} | ${reviewerRec}` : "peer";

      return `
        <tr>
          <td>${rank}</td>
          <td class="paper-cell">
            <p class="paper-title">${paper.title}</p>
            <p class="paper-sub">${paper.venue} (${paper.year}) | ${paper.method}</p>
          </td>
          <td><span class="pill ${paper.source === "ai" ? "pill-ai" : "pill-human"}">${sourceLabel(paper.source)}</span></td>
          <td>${paper.track}</td>
          <td>${paper.mu.toFixed(1)}</td>
          <td>${paper.sigma.toFixed(1)}</td>
          <td>${score}</td>
          <td>${paper.elo}</td>
          <td>${paper.matchesPlayed}</td>
          <td>${advisorText}</td>
          <td>${reviewerText}</td>
          <td class="${reviewedClass}">${reviewed}</td>
        </tr>
      `;
    })
    .join("");
}

function resolvePaperById(id) {
  return state.papers.find((paper) => paper.id === id);
}

function renderRecentMatches() {
  const mount = document.querySelector("#recent-matches");
  if (!mount) return;

  const recent = state.matches?.recentMatches ?? [];

  if (recent.length === 0) {
    mount.innerHTML = '<p class="top-meta">No recent matches logged.</p>';
    return;
  }

  mount.innerHTML = recent
    .map((match) => {
      const paperA = resolvePaperById(match.paperA);
      const paperB = resolvePaperById(match.paperB);
      if (!paperA || !paperB) return "";

      const winner =
        match.winner === "tie"
          ? "Tie"
          : match.winner === "paperA"
            ? paperA.title
            : paperB.title;

      return `
        <article class="recent-item">
          <p><strong>${paperA.title}</strong> vs <strong>${paperB.title}</strong></p>
          <p class="winner">Winner: ${winner} | ${toDateLabel(match.date)}</p>
        </article>
      `;
    })
    .join("");
}

function wireControls() {
  const sourceFilter = document.querySelector("#filter-source");
  const trackFilter = document.querySelector("#filter-track");
  const searchInput = document.querySelector("#search-title");

  if (!sourceFilter || !trackFilter || !searchInput) return;

  sourceFilter.addEventListener("change", (event) => {
    state.filters.source = event.target.value;
    renderLeaderboard();
  });

  trackFilter.addEventListener("change", (event) => {
    state.filters.track = event.target.value;
    renderLeaderboard();
  });

  searchInput.addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    renderLeaderboard();
  });
}

async function loadData() {
  const [papersResponse, matchesResponse] = await Promise.all([
    fetch("data/papers.json"),
    fetch("data/matches.json"),
  ]);

  if (!papersResponse.ok || !matchesResponse.ok) {
    throw new Error("Failed to load project data.");
  }

  const [papers, matches] = await Promise.all([
    papersResponse.json(),
    matchesResponse.json(),
  ]);

  state.papers = papers;
  state.matches = matches;
}

function renderError(message) {
  const table = document.querySelector("#leaderboard-body");
  if (table) {
    table.innerHTML = `<tr><td colspan="12">${message}</td></tr>`;
  }
}

async function init() {
  try {
    await loadData();
    fillTrackFilter();
    wireControls();
    renderStats();
    renderTopAiPapers();
    renderLeaderboard();
    renderRecentMatches();
  } catch (error) {
    renderError("Could not load leaderboard data. Check data files.");
    console.error(error);
  }
}

init();
