# Enterprise AI Development Standard (EADS)

**Version:** 0.1.0  
**Status:** Initial working release  
**Purpose:** A reusable, documentation-first delivery standard for enterprise software built with AI coding agents.

EADS combines:
- Spec-driven development and quality gates inspired by GitHub Spec Kit.
- Change proposals and living specifications inspired by OpenSpec.
- Adaptive planning and role-based review ideas inspired by BMAD.
- Repository-level agent instructions through `AGENTS.md`.
- Architecture documentation practices from arc42 and C4.
- Portable workflow packaging using the Agent Skills format.

EADS is an independent methodology. It does not require installing Spec Kit, OpenSpec, or BMAD.

## Repository layout

- `methodology/` — the EADS lifecycle, governance model and framework research.
- `project-starter/` — copy this into a new project repository.
- `skill/enterprise-ai-development/` — portable Agent Skill package.
- `scripts/` — deterministic document and approval-gate validation.
- `examples/` — illustrative examples, not production requirements.

## Quick start

1. Copy `project-starter/` into a new project repository.
2. Rename the project and fill in `docs/PROJECT_BRIEF.md`.
3. Open the repository with your coding agent.
4. Ask it to follow `AGENTS.md` and the EADS skill.
5. Complete discovery, requirements, architecture and planning reviews.
6. A human approver records the required approvals in `docs/PROJECT_STATE.json`.
7. Run the validator before authorizing implementation.

See `methodology/GETTING_STARTED.md`.

## Important control limitation

EADS instructions and local validation scripts improve process discipline; they are not a security boundary. For enforceable enterprise controls, protect approval records with repository permissions, required pull-request reviewers, branch protection/rulesets and CI checks. Production access must be controlled by infrastructure permissions, not by agent instructions.

## Versioning

EADS uses semantic versioning:
- MAJOR: incompatible workflow or artifact changes.
- MINOR: backward-compatible lifecycle, template or validation additions.
- PATCH: corrections and clarifications.

## License

Internal-use starter. Before company-wide publication, have the organization select and add its approved license and ownership notice.
