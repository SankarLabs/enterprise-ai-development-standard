# EADS lifecycle and deliverables

## Stage 0 — Initialize

Create the repository skeleton, `AGENTS.md`, project state and document index. Identify whether the project is greenfield or brownfield.

Exit: project owner, sponsor, intended users and initial project tier are identified, or explicitly recorded as unknown.

## Stage 1 — Discover

Understand the business problem, current process, users, stakeholders, outcomes, constraints, existing systems and evidence.

Artifacts:
- `PROJECT_BRIEF.md`
- `STAKEHOLDERS.md`
- `CURRENT_STATE.md` (when an existing process/system matters)
- `OPEN_QUESTIONS.md`
- `GLOSSARY.md`

Exit: business owner reviews the problem statement, scope boundary and discovery assumptions.

## Stage 2 — Define

Capture capabilities, functional requirements, business rules, workflows, data needs, non-functional requirements, acceptance criteria and out-of-scope items.

Artifacts:
- `SPEC.md`
- `BUSINESS_REQUIREMENTS.md`
- `WORKFLOWS.md`
- `NFR.md`
- `TRACEABILITY.md`
- `OPEN_QUESTIONS.md`

Exit: requirements are clear enough to estimate and design; critical questions are answered or explicitly accepted as risks.

## Stage 3 — Architect

Describe system context, containers/services, component boundaries, runtime flows, deployment view, data model, APIs, integrations, identity/security boundaries and architecture decisions.

Artifacts:
- `ARCHITECTURE.md`
- `TECH_STACK.md`
- `DATA_MODEL.md`
- `API_AND_INTEGRATIONS.md`
- `SECURITY.md`
- `docs/decisions/ADR-*.md`

Use C4 views where useful. Use arc42 as a completeness checklist, not as a requirement to fill every section with boilerplate.

Exit: technical owner/architect reviews the target architecture and material ADRs. Security, data and integration reviewers participate when relevant.

## Stage 4 — Govern

Agree coding standards, branching, test strategy, quality thresholds, observability, deployment, support, backup/recovery and operational ownership.

Artifacts:
- `CODE_STANDARDS.md`
- `TESTING_STRATEGY.md`
- `QUALITY_GATES.md`
- `DEPLOYMENT.md`
- `OPERATIONS.md`
- `RISK_REGISTER.md`

Exit: engineering and operations responsibilities are clear; security controls are identified.

## Stage 5 — Plan

Create a phased delivery plan with dependencies, estimates or sizing, risks, milestones, acceptance criteria, test evidence and rollback considerations.

Artifacts:
- `PLAN.md`
- `plans/PLAN_PHASE_*.md` for detailed phases
- `STATUS.md`

Exit: plan is reviewed; scope and sequencing are approved.

## Stage 6 — Baseline approval

A human-authorized approver reviews the required artifacts and records approval in `PROJECT_STATE.json` or the organization's approved approval system.

Gate G4 is the authorization to begin implementation. Approval must be explicit, scoped and attributable. The agent cannot approve its own work.

## Stage 7 — Implement by change

For each feature or material change:
1. Explore the existing code and current specifications.
2. Create a change proposal describing why, what, scope and impact.
3. Update affected requirements/specifications.
4. Create a design and task breakdown.
5. Review and approve the change.
6. Implement in small steps with tests.
7. Verify against acceptance criteria and traceability.
8. Update the living specification, status and decision records.
9. Archive the completed change.

Artifacts live under `changes/<change-id>/`.

## Stage 8 — Verify and operate

Complete functional, integration, security, performance and operational checks as appropriate to risk. Confirm deployment, rollback, monitoring, support ownership, data migration and user readiness.

Gate G5 authorizes a release/deployment according to organizational policy. Production deployment must still use authorized deployment controls.

## Iteration and change control

- A changed requirement must identify impacted requirements, architecture, data, APIs, tests, estimates and approvals.
- An ADR is superseded, not silently rewritten, when a material decision changes.
- The status document reports reality, not desired progress.
- Completed changes update the current specification; historical proposals remain archived.
