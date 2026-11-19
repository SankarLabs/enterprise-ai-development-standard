# Getting started with EADS

## Start a greenfield project

1. Copy `project-starter/` into a new repository.
2. Rename the project in `README.md`, `AGENTS.md` and `docs/PROJECT_BRIEF.md`.
3. Choose a project tier with the project owner.
4. Start the coding agent in the repository root.
5. Ask it to follow `AGENTS.md` and the EADS skill.
6. Complete discovery and requirements before technical design.
7. Review architecture, governance and delivery plan.
8. A human records G0–G4 approval.
9. Run `python scripts/validate_eads.py --check-gate implementation`.
10. Only then begin approved implementation work.

## Adopt EADS in an existing project

1. Inspect the repository read-only.
2. Identify current docs, code, tests, build commands, CI, integrations and deployment process.
3. Do not assume current code matches old documentation.
4. Create a gap report and map existing docs to EADS artifacts.
5. Record unknowns and conflicts.
6. Agree a baseline with the project owner.
7. Do not rewrite or reorganize the codebase merely to fit EADS.
8. Use change proposals for subsequent work.

## Suggested first prompt

"Use the EADS methodology in this repository. Read AGENTS.md and the EADS skill. Begin with Stage 1 — Discover. Ask focused questions one at a time where practical. Draft PROJECT_BRIEF.md, STAKEHOLDERS.md and OPEN_QUESTIONS.md from confirmed information. Label assumptions clearly. Do not write or modify application code, install dependencies, create infrastructure or mark approval gates approved. Stop at the G0 review and present the evidence needed for human approval."

## Approval

A human must update `docs/PROJECT_STATE.json` after reviewing the artifacts. The agent must not self-approve.
