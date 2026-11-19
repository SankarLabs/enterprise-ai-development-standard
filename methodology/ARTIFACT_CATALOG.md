# EADS artifact catalog

Artifacts are selected by project tier and risk. Required artifacts may be concise; they must not be fabricated merely to fill a template.

| Artifact | Purpose | Typical owner |
|---|---|---|
| PROJECT_BRIEF.md | Business problem, outcomes, scope and constraints | Sponsor / product owner |
| STAKEHOLDERS.md | Roles, decision rights and consultation | Project manager |
| CURRENT_STATE.md | Existing process/system baseline | Analyst / architect |
| SPEC.md | Product capabilities and functional requirements | Product owner |
| BUSINESS_REQUIREMENTS.md | Business rules, policies and outcomes | Business owner |
| WORKFLOWS.md | Current and target workflows | Analyst |
| NFR.md | Measurable quality attributes | Product + engineering |
| TRACEABILITY.md | Requirement → design → task → test links | Analyst / QA |
| ARCHITECTURE.md | Context, building blocks, runtime and deployment | Architect |
| TECH_STACK.md | Technology choices and constraints | Technical owner |
| DATA_MODEL.md | Entities, ownership, classification and lifecycle | Data owner / architect |
| API_AND_INTEGRATIONS.md | Interfaces, contracts, protocols and dependencies | Integration owner |
| SECURITY.md | Threats, identity, authorization, secrets and controls | Security |
| CODE_STANDARDS.md | Language and repository conventions | Engineering |
| TESTING_STRATEGY.md | Test levels, environments, data and evidence | QA / engineering |
| QUALITY_GATES.md | Required checks and thresholds | Engineering / QA |
| DEPLOYMENT.md | Environments, CI/CD, migration and rollback | DevOps |
| OPERATIONS.md | SLOs, monitoring, support, backup and recovery | Operations |
| RISK_REGISTER.md | Risks, mitigations, owners and residual exposure | Project manager |
| PLAN.md | Milestones, phases, dependencies and acceptance | Delivery lead |
| STATUS.md | Current implemented state and next steps | Delivery lead |
| OPEN_QUESTIONS.md | Unresolved decisions and owners | Project team |
| GLOSSARY.md | Shared domain and technical terminology | Analyst |

## Document quality rules

- Label facts, assumptions, proposals and decisions distinctly.
- Include owner, status, last-updated date and source/evidence where practical.
- Use stable IDs for requirements, risks, ADRs and changes.
- Avoid copying the same authoritative fact into multiple documents. Link to its source.
- Keep documents concise and update them when the system changes.
- Mark not-applicable items with a reason.
