# EADS framework research and design rationale

**Research snapshot:** 19 November 2026. Check official sources again before enterprise publication because projects and specifications evolve.

EADS is an independent synthesis. It borrows concepts and practices; it does not claim endorsement by or compatibility certification from the projects below.

## 1. GitHub Spec Kit

Reference: https://github.github.com/spec-kit/  
Quickstart: https://github.github.com/spec-kit/quickstart  
Repository: https://github.com/github/spec-kit

Useful ideas:
- A project constitution establishes principles once.
- A repeatable Spec → Plan → Tasks → Implement flow.
- Clarification, checklists, analysis and convergence as quality gates.
- Artifacts are Markdown and can be reviewed before implementation.

EADS adopts:
- Project principles / constitution.
- Separation of requirements from technical planning.
- Clarification and consistency review.
- Task-level acceptance criteria and implementation verification.

EADS extends:
- Enterprise discovery, stakeholder ownership and current-state analysis.
- Data governance, integration inventory, security, operations and production readiness.
- Explicit human approval records with scope and evidence.
- Traceability across business requirement, architecture, task and test.

## 2. OpenSpec

References:
- https://openspec.dev/
- https://github.com/Fission-AI/OpenSpec
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md

Useful ideas:
- Current specifications are separated from proposed changes.
- Each change is self-contained with proposal, specs, design and tasks.
- Delta specifications capture what changes instead of rewriting the whole system.
- Completed changes are archived and folded into current specifications.

EADS adopts:
- Living `specs/` and separate `changes/active/`.
- Proposal → requirements delta → design → tasks.
- Verification, synchronization and archive.

EADS extends:
- Change classification and impact assessment.
- Human approval before implementation.
- Security, data, API, migration and operational impact review.

## 3. BMAD Method

References:
- https://github.com/bmad-code-org/BMAD-METHOD
- https://docs.bmad-method.org/

Useful ideas:
- Distinct product, analysis, architecture, UX and development perspectives.
- Adaptive depth for different project sizes.
- Context preservation and validation workflows.

EADS adopts:
- Role-based review perspectives without requiring separate agent personas.
- Tiered process depth.
- Explicit product/architecture/QA/security review responsibilities.

EADS avoids:
- Mandatory multi-agent orchestration for every project.
- Large numbers of persona files when a single agent can follow a clear role checklist.
- Process complexity that exceeds project risk.

## 4. AGENTS.md

References:
- https://agents.md/
- https://github.com/agentsmd/agents.md

Useful ideas:
- A predictable repository-level instruction file for coding agents.
- Keep agent instructions separate from the human README.
- Store build, test, coding and safety conventions near the code.

EADS adopts:
- Root `AGENTS.md` as the shared repository instruction entry point.
- Optional tool-specific wrappers that point back to the shared instructions.

Limitation:
- AGENTS.md is guidance, not an approval system or security boundary.

## 5. Agent Skills

References:
- https://agentskills.io/
- https://agentskills.io/specification
- https://github.com/anthropics/skills

Useful ideas:
- Portable skill folders with a `SKILL.md`.
- Optional references, scripts and assets.
- Progressive disclosure: keep the main skill focused and load detailed references when needed.

EADS adopts:
- `skill/enterprise-ai-development/SKILL.md`.
- Detailed methodology in referenced files.
- Portable templates and validators.

Before publishing, validate the package against the current official specification and each target agent's installation conventions.

## 6. arc42

References:
- https://arc42.org/
- https://docs.arc42.org/
- https://github.com/arc42/arc42-template

Useful ideas:
- Architecture goals, constraints, context, solution strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality requirements, risks and glossary.
- Docs-as-code and right-sized architecture documentation.

EADS adopts:
- arc42 as an architecture completeness checklist.
- Concise, risk-based architecture documents rather than mandatory 12-section duplication.

## 7. C4 Model

Reference: https://c4model.com/

Useful ideas:
- System context, container, component and code views.
- Diagrams support communication, onboarding, review and risk identification.

EADS adopts:
- Context and container diagrams as the normal baseline for Tier 2/3.
- Component and dynamic/runtime views when complexity warrants them.
- Deployment diagrams for production systems.

## Synthesis

| Need | EADS source of inspiration |
|---|---|
| Project principles and spec workflow | Spec Kit |
| Change proposals and living specs | OpenSpec |
| Adaptive workflow and role perspectives | BMAD |
| Repository agent context | AGENTS.md |
| Portable workflow distribution | Agent Skills |
| Architecture completeness | arc42 |
| Architecture visualization | C4 |
| Approval governance, traceability, enterprise operations | EADS extensions |

## Research limitations

This is a practical design review, not a formal security audit, license review, procurement review or exhaustive market scan. EADS should retain links and re-check upstream documentation, supported integrations, licenses and governance before adoption.
