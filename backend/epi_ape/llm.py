from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen


@dataclass
class AdvisorResult:
    passed: bool
    score: float
    rationale: str


@dataclass
class ReviewerResult:
    score: float
    recommendation: str
    rationale: str


@dataclass
class JudgeResult:
    winner: str
    rationale: str


def _extract_json_text(raw_text: str) -> dict[str, Any] | None:
    text = (raw_text or "").strip()
    if not text:
        return None

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        chunk = text[start : end + 1]
        try:
            parsed = json.loads(chunk)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return None

    return None


def _post_json(
    url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int = 60
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=headers, method="POST")
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        text = response.read().decode(charset, errors="replace")
    return json.loads(text)


def _coerce_provider_and_model(model_name: str) -> tuple[str, str]:
    raw = model_name.strip()

    for sep in (":", "/"):
        if sep in raw:
            prefix, rest = raw.split(sep, 1)
            if (
                prefix.lower()
                in {
                    "openai",
                    "gemini",
                    "xai",
                    "grok",
                    "github",
                    "deepseek",
                }
                and rest
            ):
                provider = "xai" if prefix.lower() == "grok" else prefix.lower()
                return provider, rest

    lower = raw.lower()
    if lower.startswith(("gpt", "o1", "o3", "o4")):
        return "openai", raw
    if lower.startswith("gemini"):
        return "gemini", raw
    if lower.startswith("grok"):
        return "xai", raw
    if lower.startswith("deepseek"):
        return "deepseek", raw

    return "unknown", raw


def _extract_openai_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return str(content)


def _extract_gemini_text(payload: dict[str, Any]) -> str:
    candidates = payload.get("candidates", [])
    if not candidates:
        return ""

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    output = []
    for part in parts:
        if isinstance(part, dict) and "text" in part:
            output.append(str(part["text"]))
    return "\n".join(output)


def _gemini_keys() -> list[str]:
    keys: list[str] = []
    primary = os.getenv("GOOGLE_API_KEY", "").strip()
    fallback = os.getenv("GOOGLE_API_KEY_FALLBACK", "").strip()

    if primary:
        keys.append(primary)
    if fallback and fallback not in keys:
        keys.append(fallback)

    return keys


def _chat_json(
    model_name: str, system_prompt: str, user_prompt: str
) -> dict[str, Any] | None:
    provider, model = _coerce_provider_and_model(model_name)

    try:
        if provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                return None

            payload = _post_json(
                "https://api.openai.com/v1/chat/completions",
                {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                {
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            text = _extract_openai_text(payload)
            return _extract_json_text(text)

        if provider == "xai":
            key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
            if not key:
                return None

            payload = _post_json(
                "https://api.x.ai/v1/chat/completions",
                {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                {
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            text = _extract_openai_text(payload)
            return _extract_json_text(text)

        if provider == "gemini":
            keys = _gemini_keys()
            if not keys:
                return None

            for key in keys:
                try:
                    payload = _post_json(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                        {"Content-Type": "application/json"},
                        {
                            "contents": [
                                {
                                    "parts": [
                                        {
                                            "text": f"{system_prompt}\n\n{user_prompt}",
                                        }
                                    ]
                                }
                            ],
                            "generationConfig": {
                                "temperature": 0,
                            },
                        },
                    )
                    text = _extract_gemini_text(payload)
                    parsed = _extract_json_text(text)
                    if parsed is not None:
                        return parsed
                except Exception:
                    continue

            return None

        if provider == "github":
            token = os.getenv("GITHUB_MODELS_TOKEN") or os.getenv("GITHUB_TOKEN")
            if not token:
                return None

            url = os.getenv(
                "GITHUB_MODELS_URL",
                "https://models.inference.ai.azure.com/chat/completions",
            )
            payload = _post_json(
                url,
                {
                    "Authorization": f"Bearer {token}",
                    "api-key": token,
                    "Content-Type": "application/json",
                },
                {
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            text = _extract_openai_text(payload)
            return _extract_json_text(text)

        if provider == "deepseek":
            key = os.getenv("DEEPSEEK_API_KEY")
            if not key:
                return None

            payload = _post_json(
                "https://api.deepseek.com/chat/completions",
                {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                {
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            text = _extract_openai_text(payload)
            return _extract_json_text(text)

        return None
    except Exception:
        return None


def _bound_score(value: Any, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    return max(0.0, min(100.0, score))


def advisor_evaluate(
    model_name: str,
    paper_title: str,
    paper_track: str,
    paper_method: str,
    integrity_flags: list[str],
    paper_excerpt: str,
) -> AdvisorResult | None:
    system = (
        "You are a strict epidemiology methods advisor. "
        "Return JSON only with keys: pass (boolean), score (0-100), rationale (string)."
    )
    user = (
        f"Title: {paper_title}\n"
        f"Track: {paper_track}\n"
        f"Method: {paper_method}\n"
        f"Integrity flags: {integrity_flags}\n"
        f"Excerpt:\n{paper_excerpt}\n\n"
        "Assess fatal risks in identification, data validity, reproducibility, and inference."
    )

    payload = _chat_json(model_name, system, user)
    if not payload:
        return None

    score = _bound_score(payload.get("score"), default=0.0)
    passed = bool(payload.get("pass", score >= 66.0))
    rationale = str(payload.get("rationale", ""))[:400]
    return AdvisorResult(passed=passed, score=score, rationale=rationale)


def reviewer_evaluate(
    model_name: str,
    paper_title: str,
    paper_track: str,
    paper_method: str,
    integrity_flags: list[str],
    paper_excerpt: str,
) -> ReviewerResult | None:
    system = (
        "You are a top epidemiology reviewer. "
        "Return JSON only with keys: score (0-100), recommendation (accept|minor|major|r_and_r|reject), rationale (string)."
    )
    user = (
        f"Title: {paper_title}\n"
        f"Track: {paper_track}\n"
        f"Method: {paper_method}\n"
        f"Integrity flags: {integrity_flags}\n"
        f"Excerpt:\n{paper_excerpt}\n\n"
        "Score novelty, identification credibility, policy relevance, robustness depth, and writing clarity."
    )

    payload = _chat_json(model_name, system, user)
    if not payload:
        return None

    score = _bound_score(payload.get("score"), default=0.0)
    recommendation = str(payload.get("recommendation", "major")).strip().lower()
    if recommendation not in {"accept", "minor", "major", "r_and_r", "reject"}:
        recommendation = "major"
    rationale = str(payload.get("rationale", ""))[:400]
    return ReviewerResult(
        score=score, recommendation=recommendation, rationale=rationale
    )


def judge_pair(
    model_name: str,
    paper_a_title: str,
    paper_a_track: str,
    paper_a_method: str,
    paper_a_advisor: float,
    paper_a_reviewer: float,
    paper_b_title: str,
    paper_b_track: str,
    paper_b_method: str,
    paper_b_advisor: float,
    paper_b_reviewer: float,
) -> JudgeResult | None:
    system = (
        "You are a senior epidemiology journal editor. "
        "Return JSON only with keys: winner (paperA|paperB|tie), rationale (string)."
    )
    user = (
        "Compare two papers and select the stronger one for publication quality.\n\n"
        f"Paper A: {paper_a_title} | {paper_a_track} | {paper_a_method} | advisor={paper_a_advisor:.1f} | reviewer={paper_a_reviewer:.1f}\n"
        f"Paper B: {paper_b_title} | {paper_b_track} | {paper_b_method} | advisor={paper_b_advisor:.1f} | reviewer={paper_b_reviewer:.1f}\n"
        "Prioritize identification, robustness, and policy significance."
    )

    payload = _chat_json(model_name, system, user)
    if not payload:
        return None

    winner = str(payload.get("winner", "tie")).strip()
    if winner not in {"paperA", "paperB", "tie"}:
        winner = "tie"
    rationale = str(payload.get("rationale", ""))[:400]
    return JudgeResult(winner=winner, rationale=rationale)
