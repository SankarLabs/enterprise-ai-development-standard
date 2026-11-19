# EADS approval gates

## Gate model

| Gate | Name | Required evidence | Human decision |
|---|---|---|---|
| G0 | Project intake | Brief, owner, tier, initial risks | Accept discovery scope |
| G1 | Requirements baseline | Scope, requirements, workflows, NFRs, open questions, traceability | Approve what problem and outcomes are in scope |
| G2 | Architecture baseline | Architecture, stack, data, APIs/integrations, ADRs, security review as applicable | Approve how the system is intended to be built |
| G3 | Delivery plan | Phases, dependencies, acceptance criteria, test and rollout approach | Approve delivery approach |
| G4 | Implementation authorization | G0–G3 evidence, recorded approvals, validation results | Authorize implementation |
| G5 | Release authorization | Test evidence, security findings disposition, operational readiness, rollback, release notes | Authorize release through normal change controls |

## Strict rules

- No production implementation work before G4 approval.
- Before G4, agents may inspect an existing repository read-only, conduct discovery, draft documentation, generate diagrams, create prototypes only when explicitly authorized, and run non-mutating validation.
- No production code, schema migrations, infrastructure changes, dependency upgrades or generated application scaffolding before G4 unless separately authorized as a discovery spike.
- A discovery spike must have explicit scope, timebox, isolated branch/environment, no production impact and a cleanup plan.
- An agent may draft an approval record but must never mark a gate approved.
- A human approver must be named and authorized under company policy. The local validator rejects obvious AI/agent identities but cannot authenticate the person.
- Approvals apply to a specific scope and document baseline. Material changes invalidate affected approvals and require re-review.
- Approval in chat alone is not durable evidence. Record the decision in the repository or the organization's authoritative approval system.

## Approval record fields

Each gate record must contain:
- `status`: `pending`, `approved`, `rejected` or `not_applicable`.
- `approved_by`: human approver identity, when approved.
- `approved_at`: ISO-8601 timestamp with timezone.
- `scope`: exact baseline/change covered.
- `evidence`: document paths, review record or change/ticket identifier.
- `notes`: conditions, exceptions or rejection rationale.

## Enforcement model

Local scripts catch missing or malformed records. They do not provide tamper-proof identity or access control. Enterprise enforcement requires:
- Protected default branches and required reviewers.
- CODEOWNERS or equivalent ownership rules.
- CI checks that run validators on pull requests.
- Restricted write permissions for approval-state files.
- Separate deployment credentials and environment approvals.
- Audit logs retained by the organization's systems.

A user can edit a local JSON file. Therefore, do not claim the local gate script alone makes implementation impossible. Treat it as a workflow guardrail and connect it to protected repository controls for enforcement.
