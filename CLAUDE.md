# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install deps (uv preferred — uv.lock is the source of truth)
uv sync

# Run the app (launches Gradio UI on http://localhost:7860, also opens a public share link)
uv run deep_research.py
```

There is no test suite, linter, or build step. The app is deployed to Hugging Face Spaces automatically on push to `main` via `.github/workflows/` (which runs `gradio deploy` with a `hf_token` secret).

Required env vars in `.env`: `OPENAI_API_KEY`, `MAILJET_API_KEY`, `MAILJET_SECRET_KEY`.

## Architecture

This is a multi-agent research pipeline built on the **OpenAI Agents SDK** (`openai-agents` package, imported as `agents`). The UI is a thin Gradio wrapper; all real work happens in agents orchestrated by `ResearchManager`.

**Pipeline (sequential stages, fan-out only at search):**

`deep_research.py` (Gradio UI) → `ResearchManager.run()` → planner → searches (parallel) → writer → email

1. **`planner_agent`** — given the user query, outputs a `WebSearchPlan` (Pydantic-typed structured output) of `HOW_MANY_SEARCHES` (=5) `WebSearchItem`s. Uses `output_type=WebSearchPlan` so the SDK enforces the schema.
2. **`search_agent`** — runs once per planned search, in parallel via `asyncio.create_task` + `asyncio.as_completed`. Uses `WebSearchTool` with `tool_choice="required"` (model SDK forces the tool call). Returns a 2–3 paragraph plaintext summary. Failed searches return `None` and are silently dropped.
3. **`writer_agent`** — receives the original query plus all search summaries concatenated, returns a `ReportData` (short_summary, markdown_report, follow_up_questions). Today's date is interpolated into the system prompt at module import time, so a long-running process will see a stale date.
4. **`email_agent`** — converts the markdown report to HTML and sends via Mailjet using its `send_email` `@function_tool`. Email is optional: `email_agent.py` holds a module-global `_recipient_email` set by `set_recipient_email()` from the UI; if unset, the tool returns `{"status": "skipped"}` instead of sending. The "from" address is hardcoded in `email_agent.py:40` and must be a verified Mailjet sender.

**Streaming UX**: `ResearchManager.run` is an async generator that yields status strings between stages; the final yield is the full markdown report. Gradio rebinds the `report` Markdown component to whatever the generator yields, so each stage's status replaces the previous one until the report itself appears.

**Tracing**: `ResearchManager.run` wraps the whole pipeline in an OpenAI `trace(...)` block and prints/yields a `platform.openai.com/traces/...` URL — useful for debugging agent behavior across the multi-stage run.

## Notes for changes

- All four agents currently use `gpt-4o-mini`. Model is set per-agent in each `*_agent.py`.
- Pydantic models (`WebSearchPlan`, `WebSearchItem`, `ReportData`) are the wire format between stages — changing their fields requires updating both the producing agent's `output_type` and the consuming code in `research_manager.py`.
- The recipient-email global in `email_agent.py` is not thread/request-safe; concurrent UI sessions would race. Acceptable for the single-user demo deployment but worth knowing before scaling.

## HF Spaces deployment

**Deploy flow**: `git push origin main` → `.github/workflows/update_space.yml` runs `gradio deploy` → HF Space rebuilds. There is **no** `space` git remote anymore; HF is only reachable via the GH Action. The action makes "Upload folder using huggingface_hub" commits directly on the HF repo, so local and HF history will always drift by exactly those commits — that's normal, ignore it.

**HF force-installs `gradio[oauth,mcp]==<sdk_version>`** alongside `requirements.txt`. The `mcp` extra pins a specific `mcp` package version, and pip will fail to resolve if that pin doesn't overlap with `openai-agents`'s `mcp` constraint (currently `>=1.11.0,<2`). When upgrading `gradio`, check the new version's `mcp` extra range on PyPI first — e.g., `gradio==5.49.1` pins `mcp==1.10.1` (conflicts), `gradio==6.15.1` pins `mcp>=1.21.0,<2` (works). Bump `gradio` + `huggingface-hub` floor + run `uv lock --upgrade-package gradio` together; `uv sync` alone is a no-op if `pyproject.toml`'s range is already satisfied, and local tests will silently use the old version.

**Frontmatter conventions** (`README.md`): `sdk_version` must match the gradio pin in `requirements.txt`. `python_version` must be quoted (e.g., `"3.12"`) and ≥3.10 (the `mcp` extra has no wheels for older Python).

**Cold-start log hygiene** (visible to end users when HF wakes a sleeping Space):
- `share`/`inbrowser` in `launch()` are gated on the `SPACE_ID` env var — HF sets `SPACE_ID`, locally it's unset. Don't pass `share=True` unconditionally; it triggers a warning on HF.
- The `sys.unraisablehook` filter at the top of `deep_research.py` silences a known Python 3.12 + Gradio 6 SSR cleanup quirk (`ValueError: Invalid file descriptor: -1` from `BaseEventLoop.__del__`). Don't remove it without confirming the HF cold-start log stays clean.
