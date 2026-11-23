# Project agent instructions

## Canonical governance

This project follows the Enterprise AI Development Standard (EADS). Agent permissions, prohibited behavior, context-management requirements and human accountability are defined in `docs/AGENT_GOVERNANCE.md` — read it in full before acting. That file is a generated copy of the canonical `methodology/AGENT_GOVERNANCE.md` source maintained in the EADS standard repository; do not edit it directly. The gate model, evidence requirements and discovery-spike conditions are defined in `docs/APPROVAL_GATES.md`. That file is a generated copy of the canonical `methodology/APPROVAL_GATES.md` source maintained in the EADS standard repository; do not edit it directly. This file does not restate those rules; it adds only project-specific detail not covered there.

## Mandatory starting point

Before planning, implementing or changing this project:
1. Read this file.
2. Read `docs/AGENT_GOVERNANCE.md` and `docs/APPROVAL_GATES.md`.
3. Read `docs/PROJECT_STATE.json` and `docs/APPROVALS.md`.
4. Read the relevant project documents listed in `docs/README.md`.
5. Read the active change proposal and approval record when working on a feature.
6. If a required document is missing or conflicts with code, report the gap. Do not invent the answer.

## Project-specific operating detail

- Run `python scripts/validate_eads.py --check-gate implementation` before implementation. If the script is unavailable, stop and request review rather than assuming approval.
- For every change, use `changes/active/<change-id>/` with proposal, requirements delta, design, tasks, test plan and approval evidence.
- Keep active change documents current.
- Update current specs, traceability and STATUS.md after verification.

## Requirements and decisions

- Separate confirmed facts, assumptions, options, recommendations and decisions.
- Record unresolved questions in `docs/OPEN_QUESTIONS.md`.
- Use stable IDs: REQ-###, NFR-###, ADR-###, RISK-###, CHG-####, TASK-### and TEST-###.
- Create an ADR for material architecture decisions.

## Engineering rules

- Follow `docs/CODE_STANDARDS.md` and `docs/TESTING_STRATEGY.md`.
- Add or update tests with behavior changes.
