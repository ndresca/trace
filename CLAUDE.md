# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is
Trace is a mobile-first famous-person guessing game.
The user answers yes/probably/don't know questions. The engine narrows a
candidate set and makes a guess. Think 20 Questions meets Akinator, deterministic.

## Stack
- Engine: Python (`packages/engine/`)
- API: FastAPI (`services/api/`)
- Mobile: Expo / React Native (`apps/mobile/`) — TypeScript
- Data: JSON/JSONL (`data/`)
- iOS purchases: StoreKit via `apps/mobile/purchases.ts`
- Eval harness: `scripts/run_eval.py`
- Python deps: `requirements.txt`

## Repo Layout
packages/engine/     # Core IP — filtering, scoring, selection, models
services/api/        # FastAPI — main.py, models.py
apps/mobile/         # Expo RN app — App.tsx, purchases.ts
scripts/             # play_cli.py (dev loop), run_eval.py (eval harness)
data/questions/      # core_v1.json, exclusion_groups_v1.json
data/seeds/          # entities_v1.jsonl
data/eval/           # gold_cases_v1.json
docs/product/        # mvp.md
docs/tech/           # architecture.md, schema.md
.context/retros/     # Engineering retros (start here for history)

## Engine — Core Logic (packages/engine/)
Four modules, all deterministic:
- `filtering.py` — eliminates candidates that contradict a yes/no answer
- `scoring.py` — scores remaining candidates after each answer
- `selection.py` — picks the next best question to ask (highest signal)
- `models.py` — data models for Entity, Question, GameState

**These three files are the core IP: filtering.py, scoring.py, selection.py.
Do not refactor without running the eval harness first.**

## Data Schema
Defined in `docs/tech/schema.md`. Key files:
- `entities_v1.jsonl` — one entity per line, structured attributes
- `core_v1.json` — question bank with attribute mappings
- `exclusion_groups_v1.json` — mutually exclusive attribute groups
- `gold_cases_v1.json` — eval ground truth (expected guess per entity)

## Development Loop
Primary iteration surface:
```bash
python scripts/play_cli.py        # interactive game session
python scripts/run_eval.py        # run eval against gold_cases_v1.json
```

## Current Status (as of Apr 6, 2026)
- Engine: working — filtering, scoring, selection, early-guess logic
- CLI: working — interactive play session
- API: scaffolded — FastAPI shell exists, needs routes wired to engine
- Mobile: scaffolded — Expo shell + StoreKit purchases wired, UI minimal
- Tests: 12 test files exist, zero coverage added since project start

## Known Gaps / Active Work
1. **No unit tests on engine** — scoring.py, selection.py, filtering.py need
   tests before any new features land on top. This is priority one.
2. **API not wired to engine** — services/api/main.py is a shell.
   Needs routes: /start, /answer, /guess.
3. **Mobile UI** — App.tsx is a scaffold. Game loop not connected to API yet.

## Rules
- Never touch filtering.py, scoring.py, or selection.py without running
  run_eval.py before and after. Eval must not regress.
- Keep engine pure Python, no framework dependencies.
- API and mobile are consumers of the engine — logic stays in packages/engine/.
- When adding entities, follow the schema in docs/tech/schema.md exactly.

## Game Length

No hard question cap. The engine asks until confident.

Early exit fires on: score gap >= 1.0 OR single candidate remaining.

Avg questions is a quality metric — lower is better, but accuracy
is always the priority. Never sacrifice accuracy for speed.

## Deployment
- API: https://trace-production-1e5e.up.railway.app
- Platform: Railway (nixpacks, Python 3.11, uvicorn)
- Mobile: Expo / React Native — reads EXPO_PUBLIC_API_BASE_URL from .env
- To redeploy: railway up (from project root, service linked)

## Migration Note
Project was started with OpenAI Codex + ChatGPT. Now running on Claude.
No OpenAI API calls remain in the codebase (verify with: grep -r "openai" .).

## Suggested First Actions for Claude Code
1. Read docs/tech/architecture.md and docs/tech/schema.md
2. Run: python scripts/run_eval.py — establish baseline eval score
3. Run: python scripts/play_cli.py — one full game session to understand UX
4. Write unit tests for packages/engine/ (filtering, scoring, selection)
5. Wire services/api/main.py routes to the engine

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
