# AGENTS.md

## Project overview

Trace is a famous-person guessing game. The system asks questions, narrows candidates, and guesses the person.

## Core rules

- Standard answer set is exactly: `yes`, `probably_yes`, `i_dont_know`, `probably_no`, `no`
- Keep dependencies minimal unless explicitly approved.
- Preserve existing JSON schemas unless explicitly asked to change them.
- Do not edit unrelated files.
- Prefer small, targeted changes.

## Repo guidance

Important paths:

- `data/questions/core_v1.json`
- `data/questions/exclusion_groups_v1.json`
- `data/seeds/entities_v1.jsonl`
- `data/eval/gold_cases_v1.json`
- `packages/engine/`
- `scripts/run_eval.py`
- `scripts/play_cli.py`

## Engine guidance

- Filtering, scoring, and selection logic belong in `packages/engine`.
- CLI scripts should stay thin and reuse engine modules.
- Favor deterministic, explainable logic over complex heuristics.

## Verification

- After engine or evaluation changes, run: `python3 scripts/run_eval.py`
- After CLI-related changes, run: `python3 scripts/play_cli.py`
- Report the output briefly.

## Working style

- Use milestone-sized changes rather than many tiny edits.
- Keep code readable and minimal.
- Avoid introducing frameworks or infra unless explicitly requested.
