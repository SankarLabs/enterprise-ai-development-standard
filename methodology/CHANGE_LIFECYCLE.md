# EADS change lifecycle

EADS adopts OpenSpec's useful distinction between living specifications and proposed changes.

## Directory model

- `specs/` describes the currently approved system behavior.
- `changes/active/<change-id>/` contains proposed or in-progress changes.
- `changes/archive/` preserves completed change evidence.

## Change folder

```text
changes/active/CHG-0001-product-approval/
├── proposal.md
├── requirements-delta.md
├── design.md
├── tasks.md
├── test-plan.md
└── approval.json
```

## Workflow

1. Explore: understand current code, docs and behavior.
2. Propose: record problem, value, scope, exclusions and impact.
3. Specify: add, modify or retire requirement statements and scenarios.
4. Design: document implementation approach and affected components.
5. Task: create ordered, testable tasks with owners/dependencies.
6. Approve: human approves change scope and design before implementation.
7. Apply: implement tasks and tests.
8. Verify: compare implementation with requirements and design; run checks.
9. Sync: update current `specs/` to reflect verified behavior.
10. Archive: retain proposal, approval, verification evidence and outcome.

## Change classes

- Minor: implementation detail with no externally observable behavior change.
- Standard: new or changed user-visible/system behavior.
- Significant: security, data model, integration contract, architecture, compliance, availability or migration impact.
- Emergency: follows the organization's emergency change process; document retrospective evidence.

Classification is a recommendation by the agent and must be confirmed by the authorized owner.
