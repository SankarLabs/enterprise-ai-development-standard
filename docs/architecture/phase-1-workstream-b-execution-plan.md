# EADS v0.2 — Phase 1, Workstream B: Execution Plan

**Status:** Planning document only. **Not implemented.** No Workstream B schema, YAML, or `PROJECT_STATE.json` content has been created or modified by this document. Nothing here is active policy, an approved schema, or a ratified organizational decision.
**Primary source:** `docs/architecture/phase-1-workstream-b-decision-assessment.md`, committed at `f852893b9226baf9acfba1c03365c081d5fc8eb8` on `feature/eads-v0.2` — this plan sequences and operationalizes that assessment's decisions, dependencies, and milestones. It does not re-derive, re-litigate, or revise them.
**Architectural baseline:** `docs/architecture/phase-1-structured-core-policy-design.md` (Revision 8, approved); `docs/architecture/phase-1-workstream-a-implementation-plan.md` (approved); `core/` as committed at `4231a657fc8fde706c4febf7faf7f43eb7f17467` (Workstream A).
**Scope:** Execution sequencing and operational detail for Workstream B only. Does not implement any milestone, does not touch Workstream C, does not touch Runtime (Phase 2+), and does not modify Revision 8, the Workstream A plan, or any file under `core/`.

---

## 0. Repository inspection (performed for this plan)

- Branch: `feature/eads-v0.2`.
- HEAD at time of writing: `f852893b9226baf9acfba1c03365c081d5fc8eb8` — `docs(eads): add Phase 1 Workstream B decision assessment`.
- Working tree: clean before this document was added.
- `main` and tag `v0.1.0`: both at `73eb3f75b3f39e02bf77dcf364bbaa72f2cc626e`; `git diff main v0.1.0` is empty — unchanged.
- `docs/architecture/phase-1-structured-core-policy-design.md`, `docs/architecture/phase-1-workstream-a-implementation-plan.md`, and `core/` all last modified at commit `4231a65` (Workstream A) — confirmed unchanged since, via `git log -1 -- <path>`.
- `methodology/` last modified at commit `9a1d55c` (Phase 0) — confirmed unchanged.

No incompatibility between the committed Workstream B assessment and the current state of Revision 8 / Workstream A / `core/` was found during this inspection. **No Workstream A decision or schema requires revision as a precondition for this plan.**

---

## 1. Purpose and scope

This document turns the approved Workstream B decision assessment into an **execution-ready plan**: every milestone (`WB-1`–`WB-26`, including the lettered sub-milestones and the retirement note) gets a deliverable, an acceptance criterion, an affected-file list, and an explicit dependency statement, organized into logical execution groups with parallelism called out.

This plan does **not**:
- Resolve any of the nine organizational questions in the assessment's Section 6.
- Invent authority-domain values, identity mappings, tier requirements, gate-artifact associations, lifecycle-stage ratification, change-classification values, or any other organizational input. Every point where such input is required is marked **`PENDING_ORGANIZATIONAL_INPUT`** (Section 6 of this document) rather than filled in or assumed.
- Implement any schema, YAML file, script, or `PROJECT_STATE.json` change.
- Begin Workstream C (integration, ratification) or any Runtime (Phase 2+) component.
- Reintroduce the retired `WB-11b`/`WB-12b` milestones, renumber any milestone, or alter any dependency the assessment established.

---

## 2. Source documents and architectural constraints

| Document | Role | Constraint this plan honors |
|---|---|---|
| `phase-1-workstream-b-decision-assessment.md` (commit `f852893`) | Primary source for scope, decisions, dependencies, milestones | This plan's milestone IDs, deliverables, and dependencies are taken verbatim from Section 7; no milestone is added, removed, or renumbered beyond what the assessment itself already retired. |
| `phase-1-structured-core-policy-design.md` (Revision 8) | Approved architecture baseline | Not modified. Every schema shape this plan references (manifest, governance-rule, evidence-requirement, authority-requirement, lifecycle-stage, approval-gate, artifact, change-classification, capability, evaluation-spec) traces to a specific Revision 8 section, cited inline where relevant. |
| `phase-1-workstream-a-implementation-plan.md` | Approved Workstream A plan | Not modified. Workstream A's seven schemas and `core/governance.yaml`'s 28 rules are treated as a stable, committed foundation that Workstream B extends, not revises. |
| `core/` (commit `4231a65`) | Committed Workstream A policy bundle | Not modified by this plan. The file-impact matrix (Section 7) identifies exactly which Workstream A files Workstream B's *eventual implementation* will touch, and why — this plan does not touch them itself. |
| `methodology/AGENT_GOVERNANCE.md`, `methodology/APPROVAL_GATES.md`, `methodology/LIFECYCLE.md`, `methodology/ARTIFACT_CATALOG.md`, `methodology/CHANGE_LIFECYCLE.md`, `project-starter/docs/PROJECT_STATE.json` | Existing v0.1 prose and project-state shape | Referenced for grounding only, as the assessment itself does; not modified. |

**Boundary this plan enforces throughout:** Core policy (`core/`), project configuration (`PROJECT_STATE.json` and its planned extensions), and Runtime behavior (Phase 2+) remain three distinct layers. A schema *designed* in Workstream B is not a Runtime *capability* — consistent with Revision 8's own Section 9/12 correction, which this plan does not reopen.

---

## 3. Workstream B decision summary — all eleven decisions

| ID | Area | One-line summary | Organizational input required? |
|---|---|---|---|
| `WB-D1` | 3.1 | Gate↔artifact associations for all 23 cataloged artifacts | Yes — `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-D2` | 3.2 | Whether to enumerate authority domains, and if so, which values | Yes — `PENDING_ORGANIZATIONAL_INPUT` (critical path) |
| `WB-D3` | 3.2 | Where/how a project records domain→identity mapping | Yes — `PENDING_ORGANIZATIONAL_INPUT` (depends on `WB-D2`) |
| `WB-D4` | 3.2 | Per-gate `supported_authority_models` (local/external) eligibility | Yes — `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-D5` | 3.3 | Ratify (or re-validate) `STAGE-0`..`STAGE-8` lifecycle-stage IDs | Yes, but minimal — `PENDING_ORGANIZATIONAL_INPUT` (content already exists in `LIFECYCLE.md`) |
| `WB-D6` | 3.4 | Tier-specific `by_tier` status (23 artifacts × 3 tiers = 69 values) | Yes — `PENDING_ORGANIZATIONAL_INPUT` (highest volume) |
| `WB-D7` | 3.5 | `gate_impact` shape, then its per-class values | Yes — `PENDING_ORGANIZATIONAL_INPUT` (shape itself unsettled by Revision 8) |
| `WB-D8` | 3.6 | `GOV-013`/`EXC-001` migration, incl. `authorized_by_domain` value | Yes, partially — `PENDING_ORGANIZATIONAL_INPUT` for the domain value (depends on `WB-D2`); the condition-field confirmation is a lightweight review, not invention |
| `WB-D9` | 3.7 | Project-level authorization-record schema (layer 3) | Design decision only once `WB-D2`/`WB-D3`/`WB-D8` land — schema itself is engineering, not organizational, once inputs exist |
| `WB-D10` | 3.7 | Conditional-resolution-record schema (`content_snapshot`) | Minimal — "closer to pure schema engineering" per the assessment |
| `WB-D11` | 3.7 | `PROJECT_STATE.json` version-split / project-adoption record | Low — bookkeeping/schema question, not a policy judgment |

All eleven are addressed in the milestone plan (Section 8) and the organizational input register (Section 6).

---

## 4. Dependency overview

Reproduced from the assessment's Section 5, unchanged:

- **Critical path (fork-then-join):** `WB-D2` precedes `WB-D3` and `WB-D8` independently; `WB-D3` and `WB-D8` do not depend on each other and can proceed in parallel once `WB-D2` lands; `WB-D9` is the join point requiring all three.
- **Independent Track 2:** `WB-D1`, `WB-D5`, `WB-D6`, `WB-D7` have no dependency on `WB-D2` or on each other, and can be resolved and even implemented entirely in parallel with Track 1.
- **Low-coupling schema work:** `WB-D10`, `WB-D11` depend on nothing organizational; they can be drafted immediately.

**Work that can proceed before any organizational input arrives** (no decision pending): drafting `approval-gate.schema.json`'s structure (`WB-11a`), `artifact.schema.json`'s structure (`WB-12a`), the conditional-resolution-record schema (`WB-9`), `PROJECT_STATE.json`'s version-split/adoption-record structure (`WB-10`), and a non-binding skeleton of the project-level authorization-record schema (`WB-15a`).

**The single most-blocking decision:** `WB-D2` (via milestone `WB-1`). It gates `WB-6` (`WB-D3`), `WB-16` (`WB-D8`'s migration), `WB-14` (the conditional schema modification), `WB-18` (gate content), and transitively `WB-15b`/`WB-D9` (the join). Resolving `WB-D2` first and resolving it correctly is the single highest-leverage action available to unblock the rest of Workstream B.

---

## 5. Execution groups (Step 4 sequencing)

Five groups, as requested. Each milestone appears in exactly one group below; its full detail (deliverable, acceptance criteria, files, dependencies) is in Section 8's milestone table. Group placement reflects *when work can start*, not the assessment's own Section 7 category labels (Organizational decisions / Schema design / Policy data migration / Cross-record validation / Human review) — both groupings are shown side by side in Section 8 so the mapping is traceable.

### Group 1 — Preparatory and independent schema work (no organizational prerequisite; start immediately, fully parallel)
`WB-9`, `WB-10`, `WB-11a`, `WB-12a`, `WB-15a`

### Group 2 — Authority and approval decision track (the `WB-D2` critical path cluster, plus `WB-D4`, which is thematically authority/approval but has no hard dependency on `WB-D2`)
`WB-1` → (`WB-6`, `WB-8` in parallel) → `WB-16` → `WB-15b`; `WB-14` (gated on `WB-1`); `WB-7` (independent, may run anywhere in this window); `WB-18` (gated on `WB-1`, `WB-7`, `WB-11a`, `WB-14`)

### Group 3 — Artifact, tier, lifecycle, and change-classification track (fully independent of Group 2; can run entirely in parallel with it)
`WB-2`, `WB-3`, `WB-4`, `WB-5`, `WB-13`, `WB-17`, `WB-19`, `WB-20`

### Group 4 — Cross-file validation and consistency checks (requires both Group 2 and Group 3 content to exist)
`WB-21` → `WB-22` → `WB-23`

### Group 5 — Workstream B completion review (requires everything above)
`WB-24`, `WB-25`, `WB-26`

```
Group 1 (parallel, no prerequisite)
  WB-9  WB-10  WB-11a  WB-12a  WB-15a
                 |        |
Group 2 (authority/approval)          Group 3 (artifacts/tier/lifecycle/change-class)
  WB-1 ──┬── WB-6 ──────────┐           WB-2  WB-3  WB-4  WB-5
         ├── WB-8 ── WB-16 ─┼─ WB-15b    |     |          |
         └── WB-14 ─────────┘           WB-17 WB-19(*)  WB-13
  WB-7 (independent)                     (*WB-19 also needs WB-2,WB-3,WB-12a,WB-17,WB-18)
  WB-18 (needs WB-1,WB-7,WB-11a,WB-14)   WB-20 (needs WB-13, WB-18)
         \_______________________________/
                        |
Group 4: WB-21 → WB-22 → WB-23
                        |
Group 5: WB-24, WB-25, WB-26
```

---

## 6. Organizational input register

Every row below corresponds 1:1 to a Section 6 question in the committed assessment. **No value is proposed here.** Status is `PENDING_ORGANIZATIONAL_INPUT` for all nine; this plan does not and must not resolve them.

| # | Question (verbatim intent) | Decision | Blocks milestone(s) | Status |
|---|---|---|---|---|
| 1 | Enumerate authority domains at all, or require only an authenticated decision with no taxonomy? | `WB-D2` | `WB-1`, and transitively `WB-6`, `WB-14`, `WB-16`, `WB-18`, `WB-15b` | `PENDING_ORGANIZATIONAL_INPUT` |
| 2 | If enumerated, what are the domain values, and who decides? | `WB-D2` | Same as above | `PENDING_ORGANIZATIONAL_INPUT` |
| 3 | Where/how is the domain→identity mapping recorded? | `WB-D3` | `WB-6`, transitively `WB-15b` | `PENDING_ORGANIZATIONAL_INPUT` |
| 4 | Per-gate, should evidence be acceptable from `local`, `external`, or both? | `WB-D4` | `WB-7`, transitively `WB-18` | `PENDING_ORGANIZATIONAL_INPUT` |
| 5 | Per-artifact, which gate(s) actually require it, in real practice? | `WB-D1` | `WB-2`, transitively `WB-19` | `PENDING_ORGANIZATIONAL_INPUT` |
| 6 | Per-artifact, per-tier: required / conditional / optional / not applicable, and under what condition? | `WB-D6` | `WB-3`, transitively `WB-19` | `PENDING_ORGANIZATIONAL_INPUT` |
| 7 | Ratify `LIFECYCLE.md`'s existing Stage 0–8 content as `STAGE-0`..`STAGE-8`, or re-validate first? | `WB-D5` | `WB-4`, transitively `WB-17`, `WB-19` | `PENDING_ORGANIZATIONAL_INPUT` |
| 8 | What should a change classification *do* to gate approvals, and which class does which? | `WB-D7` | `WB-5`, transitively `WB-13`, `WB-20` | `PENDING_ORGANIZATIONAL_INPUT` |
| 9 | Does `GOV-013`/`EXC-001`'s structured representation match actual reviewer practice today? | `WB-D8` | `WB-8`, transitively `WB-16` | `PENDING_ORGANIZATIONAL_INPUT` (confirmation-only; does not require inventing new content — see assessment Section 3.6) |

**No decision owner is assigned** in this register, consistent with the assessment's explicit position (Section 3 preamble; Section 9) that EADS does not invent a role taxonomy. Each organization must designate who answers each row.

---

## 7. File impact matrix

Reproduced and operationalized from the assessment's Section 4, with the milestone that touches each file.

### Core policy files (`core/`)

| File | Status | Milestone | Governing schema |
|---|---|---|---|
| `core/gates.yaml` | New | `WB-18` | `core/schema/approval-gate.schema.json` (new, `WB-11a`) |
| `core/artifacts.yaml` | New | `WB-19` | `core/schema/artifact.schema.json` (new, `WB-12a`) |
| `core/lifecycle.yaml` | New | `WB-17` | `core/schema/lifecycle-stage.schema.json` (existing, Workstream A — no new schema milestone needed) |
| `core/change-classification.yaml` | New | `WB-20` | `core/schema/change-classification.schema.json` (new, `WB-13`) |
| `core/governance.yaml` | Modified (additive — `GOV-013`/`EXC-001` appended; no existing rule content changed) | `WB-16` | `core/schema/governance-rule.schema.json` (existing, Workstream A, unmodified by this append) |
| `core/manifest.yaml` | Modified (`files` list, `policy_version`, `compatible_schema_versions`) | `WB-21` | `core/schema/manifest.schema.json` (existing, Workstream A, unmodified) |

### JSON Schemas (`core/schema/`)

| File | Status | Milestone | Notes |
|---|---|---|---|
| `core/schema/approval-gate.schema.json` | New | `WB-11a` | Consumes `evidence-requirement.schema.json` and `authority-requirement.schema.json` as nested types (both Workstream A). |
| `core/schema/artifact.schema.json` | New | `WB-12a` | References `lifecycle-stage.schema.json`'s `artifact_refs` target and `approval-gate.schema.json`'s gate IDs. |
| `core/schema/change-classification.schema.json` | New | `WB-13` | Its `gate_impact` field shape is itself `PENDING_ORGANIZATIONAL_INPUT` (question 8) — gated on `WB-5`. |
| `core/schema/authority-requirement.schema.json` | **Conditionally modified** — `enum` added to `domain` **only if** `WB-D2` resolves "enumerate" | `WB-14` | If `WB-D2` resolves "do not enumerate," **no change to this file at all**. This is the one Workstream A schema this plan anticipates touching, exactly as the assessment flags (Section 4.2) — not a newly found incompatibility. |
| `core/schema/governance-rule.schema.json` (`Exception.authorized_by_domain`) | **Conditionally modified or left as-is**, pending a design decision on `$ref`-based convergence with `authority-requirement.schema.json` | `WB-14` | Explicitly an *open schema-design question the assessment surfaces*, not a Revision 8 answer — this plan does not resolve it here; `WB-14`'s acceptance criteria require the decision be made explicitly, one way or the other, and recorded. |
| `core/schema/manifest.schema.json`, `evidence-requirement.schema.json`, `capability.schema.json`, `evaluation-spec.schema.json`, `lifecycle-stage.schema.json` | **No change anticipated** | — | Per assessment Section 4.2, explicitly confirmed unaffected. |

### Project-level / project-configuration files (outside `core/`)

| File | Status | Milestone | Notes |
|---|---|---|---|
| A project-level authorization-record schema | New, **location not yet determined** | `WB-15a` (skeleton), `WB-15b` (finalize) | Per assessment Section 4.1/14 item 8: "named, not designed" — this plan does not propose a location. Flagged as an open implementation question (Section 10). |
| A conditional-resolution-record schema | New, **location not yet determined** | `WB-9` | Same caveat as above. |
| `project-starter/docs/PROJECT_STATE.json` | Structural additions (version-field split, project-adoption record) | `WB-10` | Low organizational coupling; primarily a bookkeeping/schema question. |

### Validation scripts (`scripts/`)

| File | Status | Milestone | Notes |
|---|---|---|---|
| `scripts/check_governance_ids.py` | **Unmodified** — re-run as-is | `WB-23` | Assessment explicitly states "no new tooling needed for this specific check." |
| A Core-internal schema + cross-file reference-integrity validator (name/location not specified by the assessment) | New or extended | `WB-22` | The assessment describes *what* `WB-22` must check (eight-file schema validation plus three cross-file reference checks) but does not name an implementation artifact. This plan does not invent one; flagged as an open engineering decision in Section 10 (not organizational — naming/placing a validation script is an engineering choice, consistent with existing `scripts/` precedent, not a policy decision). |

**No file outside this matrix is touched by Workstream B**, per the assessment's own scope exclusions (Section 9) and this plan's Section 1.

---

## 8. Milestone-by-milestone execution plan

Every milestone from the assessment's Section 7, in its approved dependency order. The "Assessment group" column shows the original Section 7 heading for traceability; "Plan group" shows this document's Section 5 grouping.

| ID | Assessment group | Plan group | Deliverable | Depends on | Acceptance criteria | Files affected | Org input |
|---|---|---|---|---|---|---|---|
| `WB-1` | Organizational decisions | Group 2 | Resolve `WB-D2`: enumerate authority domains or not; if so, values | None | A recorded, attributable organizational decision exists, stating either a closed enum of domain values or "no enum — free string by convention." | None directly (gates `WB-6`, `WB-14`, `WB-16`, `WB-18`) | **`PENDING_ORGANIZATIONAL_INPUT`** |
| `WB-2` | Organizational decisions | Group 3 | Resolve `WB-D1`: gate↔artifact associations for all 23 artifacts | None | A recorded mapping exists, per artifact, of which G0–G5 gate(s) require it, with rationale traceable to real review practice (not derived mechanically without human confirmation). | None directly (gates `WB-19`) | **`PENDING_ORGANIZATIONAL_INPUT`** |
| `WB-3` | Organizational decisions | Group 3 | Resolve `WB-D6`: tier-specific `by_tier` values, all 23 artifacts × 3 tiers | None | All 69 status values recorded (`required`/`conditional`/`optional`/`not_applicable`), each `conditional` entry carrying a non-empty `condition` string, each other status carrying none. Values reflect genuine per-artifact judgment, not template-filling (assessment Section 3.4 risk). | None directly (gates `WB-19`) | **`PENDING_ORGANIZATIONAL_INPUT`** |
| `WB-4` | Organizational decisions | Group 3 | Resolve `WB-D5`: ratify or re-validate lifecycle-stage IDs | None | A recorded decision either ratifies `LIFECYCLE.md`'s Stage 0–8 content as `STAGE-0`..`STAGE-8` directly, or documents a re-validation pass and its outcome. | None directly (gates `WB-17`) | **`PENDING_ORGANIZATIONAL_INPUT`** (minimal effort expected) |
| `WB-5` | Organizational decisions | Group 3 | Resolve `WB-D7`'s shape question, then its values | None | A recorded decision on what `gate_impact` structurally means (e.g., per-class list of invalidated gate IDs), followed by which of the four change classes trigger which effect. | None directly (gates `WB-13`, `WB-20`) | **`PENDING_ORGANIZATIONAL_INPUT`** (two-staged: shape, then values) |
| `WB-6` | Organizational decisions | Group 2 | Resolve `WB-D3`: domain→identity mapping location/shape | `WB-1` | A recorded decision on where and how the domain→identity mapping lives (e.g., CODEOWNERS-style, access-control system, YAML list) — shape may differ entirely depending on `WB-1`'s outcome. | None directly (gates `WB-15b`) | **`PENDING_ORGANIZATIONAL_INPUT`** |
| `WB-7` | Organizational decisions | Group 2 | Resolve `WB-D4`: per-gate `supported_authority_models` | None (independent of `WB-1`/`WB-2`) | A recorded `local`/`external`/both decision per gate (G0–G5). | None directly (gates `WB-18`) | **`PENDING_ORGANIZATIONAL_INPUT`** |
| `WB-8` | Organizational decisions | Group 2 | Confirm `GOV-013`'s structured fields against actual reviewer practice | None | A reviewer confirms (or revises) the condition fields against real discovery-spike evaluation practice; this is a lightweight review, not new invention, per the assessment. | None directly (gates `WB-16`) | **`PENDING_ORGANIZATIONAL_INPUT`** (confirmation-level) |
| `WB-9` | Schema design | Group 1 | Draft the conditional-resolution-record schema (`WB-D10`) | None | Schema fully specifies the `content_snapshot`/`schema_version`/resolution-decision fields per Revision 8 Section 5.5.1's already-settled comparison mechanics. Valid JSON Schema document. | New schema, location TBD (Section 10) | None — can start immediately |
| `WB-10` | Schema design | Group 1 | Draft `PROJECT_STATE.json`'s version-split/project-adoption additions (`WB-D11`) | None | Draft fields for split `schema_version`/`policy_version` tracking and a project-adoption record exist and are internally consistent with Revision 8 Section 5.1/10. | `project-starter/docs/PROJECT_STATE.json` (draft additions) | None — can start immediately |
| `WB-11a` | Schema design | Group 1 | Draft `approval-gate.schema.json`'s structure | None | Valid JSON Schema; shape matches Revision 8 Section 5.4 ("unchanged in shape from revision 1"); correctly consumes `evidence-requirement.schema.json` and `authority-requirement.schema.json` as nested types (verify `$ref`-based composition per the retirement note below). | `core/schema/approval-gate.schema.json` (new) | None — can start immediately |
| `WB-12a` | Schema design | Group 1 | Draft `artifact.schema.json`'s structure | None | Valid JSON Schema; `by_tier` status-map shape matches Revision 8 Section 5.5 exactly (tier-completeness required; `condition` mandatory only on `conditional`). | `core/schema/artifact.schema.json` (new) | None — can start immediately |
| `WB-13` | Schema design | Group 3 | Author `change-classification.schema.json` | `WB-5` | Valid JSON Schema; `gate_impact`'s shape matches whatever `WB-5` records (shape and values cannot be separated here, per assessment Section 3.5). | `core/schema/change-classification.schema.json` (new) | Inherits `WB-5`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-14` | Schema design | Group 2 | Modify `authority-requirement.schema.json`'s `domain` enum **only if** `WB-1` resolved "enumerate"; resolve the `Exception.authorized_by_domain` convergence question explicitly | `WB-1` | If "enumerate": `enum` added with exactly `WB-1`'s recorded values, no more, no fewer. If "do not enumerate": explicit confirmation that no change was made, recorded as a reviewable decision in its own right (not silently skipped). Either way, the `$ref`-vs-independent-definition convergence question (assessment Section 4.2) is resolved explicitly, not left implicit. | `core/schema/authority-requirement.schema.json` (conditional); `core/schema/governance-rule.schema.json` (conditional, convergence decision) | Inherits `WB-1`'s `PENDING_ORGANIZATIONAL_INPUT` for the enum values |
| `WB-11/12 retirement note` | Schema design | Group 1/2 (cross-cutting) | No independent deliverable — a standing constraint on `WB-11a`/`WB-12a`/`WB-14`: confirm `$ref`-based composition when drafting `WB-11a` (or resolve nested-schema composition within `WB-11a` if the approved contract does not use `$ref`); `WB-2`/`WB-3` affect `artifact.schema.json`'s content values only, never its structure. | N/A | Verified as part of `WB-11a`'s and `WB-14`'s own acceptance criteria above — **not re-introduced as a separate milestone**, and `WB-11b`/`WB-12b` remain retired. | None (constraint only) | None |
| `WB-15a` | Schema design | Group 1 | Sketch a non-binding skeleton of the project-level authorization-record schema (`WB-D9`) | None | A discussion-only draft exists (citing-exception-id, authorizing-identity, scope/timebox/branch/cleanup-plan fields) — explicitly not finalized, explicitly not treated as approved. | New schema skeleton, location TBD (Section 10) | None — discussion draft only |
| `WB-16` | Policy data migration | Group 2 | Migrate `GOV-013`/`EXC-001` into `core/governance.yaml` | `WB-1`, `WB-8` | New rule appended with exactly the Revision 8 worked-example shape (Section 5.2), `authorized_by_domain` set to `WB-1`'s recorded value/convention, `condition` text matching `WB-8`'s confirmed fields. No existing rule's content altered. Validates against `governance-rule.schema.json`. `check_governance_ids.py` run against the updated file confirms no `GOV-###`/`EXC-###` duplication. | `core/governance.yaml` (additive) | Inherits `WB-1`/`WB-8`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-15b` | Policy data migration | Group 2 | Finalize the project-level authorization-record schema | `WB-1`, `WB-6`, `WB-16` | Schema's domain-citation field matches `WB-1`'s enum-or-not outcome exactly (ID lookup vs. free-text convention); identity-side field shape matches `WB-6`'s decision; a worked example validates by citing the real `EXC-001` from `WB-16`. | New schema, location TBD (Section 10) | Inherits `WB-1`/`WB-6`/`WB-8`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-17` | Policy data migration | Group 3 | Author `core/lifecycle.yaml` content | `WB-4` | All nine stages (`STAGE-0`..`STAGE-8`) authored exactly per `WB-4`'s ratified/re-validated content; validates against the existing `lifecycle-stage.schema.json`. | `core/lifecycle.yaml` (new) | Inherits `WB-4`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-18` | Policy data migration | Group 2 | Author `core/gates.yaml` content | `WB-1`, `WB-7`, `WB-11a`, `WB-14` | All six gates (G0–G5) authored with `authority_requirement.domain` matching `WB-1`'s outcome and `supported_authority_models` matching `WB-7`'s per-gate decisions; validates against `approval-gate.schema.json`. | `core/gates.yaml` (new) | Inherits `WB-1`/`WB-7`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-19` | Policy data migration | Group 3 | Author `core/artifacts.yaml` content | `WB-2`, `WB-3`, `WB-12a`, `WB-17`, `WB-18` | All 23 artifacts authored with `gate_associations` matching `WB-2` and `by_tier` matching `WB-3` exactly; `gate_associations` resolve to real IDs from `WB-18`; any `artifact_refs` consumers in `WB-17` resolve correctly; validates against `artifact.schema.json`. | `core/artifacts.yaml` (new) | Inherits `WB-2`/`WB-3`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-20` | Policy data migration | Group 3 | Author `core/change-classification.yaml` content | `WB-13`, `WB-18` | All four change classes authored with `gate_impact` values matching `WB-5`'s decision, referencing real gate IDs from `WB-18`; validates against `change-classification.schema.json`. | `core/change-classification.yaml` (new) | Inherits `WB-5`'s `PENDING_ORGANIZATIONAL_INPUT` |
| `WB-21` | Policy data migration | Group 4 | Update `core/manifest.yaml`'s `files` list, `policy_version`, `compatible_schema_versions` | `WB-16`–`WB-20` | `files` lists exactly the files added/modified above; `policy_version` bumped per Revision 8 Section 10's rule; `compatible_schema_versions` updated only where Section 5.1's dual-guarantee test (loadable *and* snapshot-safe) is deliberately evaluated and satisfied — never added by default. `lifecycle_state` remains `draft`. | `core/manifest.yaml` (modified) | None directly (consumes outputs of prior `PENDING_ORGANIZATIONAL_INPUT` items) |
| `WB-22` | Cross-record validation | Group 4 | Core-internal validation: **(a)** all eight Core YAML files against their schemas; **(b)** cross-file reference integrity (`scope.reference`, `gate_associations`, `artifact_refs` resolve to real IDs) | `WB-17`–`WB-21` | All eight files (`manifest.yaml`, `governance.yaml`, `capabilities.yaml`, `evaluation.yaml`, `gates.yaml`, `artifacts.yaml`, `lifecycle.yaml`, `change-classification.yaml`) pass schema validation; all cross-file references resolve; exit code / report format documented at implementation time (Section 10). No Runtime invoked. | A Core-internal validator, name/location TBD (Section 10) | None directly |
| `WB-23` | Cross-record validation | Group 4 | Confirm `EXC-###` uniqueness after `EXC-001` is added | `WB-16` | `scripts/check_governance_ids.py core/governance.yaml` exits 0, reporting the updated unique `GOV-###`/`EXC-###` counts. No code change to the script. | `scripts/check_governance_ids.py` (unmodified, re-run) | None |
| `WB-24` | Human review | Group 5 | Per-area review after each organizational decision (`WB-1`–`WB-8`) lands, before consuming work begins | `WB-1`–`WB-8` (per-area, not all at once) | A reviewer confirms each decision matches Revision 8's constraints (e.g., `WB-D2`'s enum, if any, doesn't reintroduce named roles) before `WB-9`-and-later work consuming it starts. | None (review gate) | N/A (review of prior `PENDING_ORGANIZATIONAL_INPUT` resolutions) |
| `WB-25` | Human review | Group 5 | Fidelity review: every migrated value traces to its organizational decision record | `WB-16`–`WB-20` | For each of `core/gates.yaml`, `core/artifacts.yaml`, `core/lifecycle.yaml`, `core/change-classification.yaml`, and `GOV-013`/`EXC-001`, a reviewer confirms every field value traces to a recorded organizational decision, with no invented value anywhere. | None (review gate) | N/A |
| `WB-26` | Human review | Group 5 | Full Workstream B acceptance pass | All prior milestones | **(1)** all JSON Schema documents syntactically valid; **(2)** every Core YAML file validates against its schema; **(3)** all cross-record checks (`WB-22`, `WB-23`) pass; `core/manifest.yaml.lifecycle_state` remains `draft`; no file outside this plan's matrix (Section 7) was touched. | None (acceptance gate) | N/A |

**Milestone-ID fidelity check:** 27 `WB-N`-labeled milestones (`WB-1`–`WB-10`, `WB-11a`, `WB-12a`, `WB-13`, `WB-14`, `WB-15a`, `WB-16`, `WB-15b`, `WB-17`–`WB-26`) plus the one retirement note — **28 total**, matching the committed assessment exactly. No milestone ID was changed, renumbered, or reintroduced from retirement.

---

## 9. Validation and acceptance criteria (consolidated)

Beyond each milestone's own acceptance criteria (Section 8), Workstream B as a whole requires, before `WB-26` can pass:

1. **Schema validity** — every new/modified JSON Schema (`approval-gate`, `artifact`, `change-classification`, conditionally `authority-requirement` and `governance-rule`, plus the two project-level schemas) is well-formed JSON and a valid JSON Schema document (Draft 2020-12, consistent with Workstream A's own validation approach).
2. **Content validity** — every Core YAML file (new and modified) validates against its governing schema.
3. **Cross-file reference integrity** — every `scope.reference`, `gate_associations`, and `artifact_refs` entry resolves to a real ID within the Core bundle. (`agent-adapter`-dimension scope references remain unvalidatable, per Revision 8's own acknowledged limitation — no adapter registry exists in Phase 1.)
4. **Cross-record uniqueness regression** — re-running `check_governance_ids.py` against the post-`WB-16` `core/governance.yaml` must still report the correct unique count; this is a **regression check** against Workstream A's own established tooling, not new tooling.
5. **Fidelity traceability** — every organizational-input-derived value traces to a recorded decision (`WB-25`); no value is present in any Core file without a corresponding register entry (Section 6) being resolved.
6. **Manifest integrity** — `core/manifest.yaml`'s `files` list, `policy_version`, and `compatible_schema_versions` accurately reflect the bundle state; `lifecycle_state` never advances past `draft` during Workstream B (that transition is Workstream C's, explicitly out of scope here).
7. **Scope containment** — no file outside the Section 7 impact matrix was touched; no Runtime component was built; Workstream C's integration pass was not started.

---

## 10. Risks, assumptions, and unresolved questions

### Risks (carried forward from the assessment's Section 8, unchanged)

| Risk | Severity |
|---|---|
| `WB-D2` decided too late or inconsistently, forcing rework of `WB-D3`, `WB-D8`, `WB-D9` | High |
| Workstream B breaks the "strictly additive" invariant without anyone noticing `core/manifest.yaml` / `authority-requirement.schema.json` need modification | Medium |
| `Exception.authorized_by_domain` and `authority-requirement.domain` drift into two differently-constrained notions of "domain" | Medium |
| Tier-specific requirements (`WB-D6`) filled in as template-completion rather than genuine judgment | Medium |
| `gate_impact`'s shape treated as already-settled when it is not | Medium |
| `GOV-013` migrated with a guessed `authorized_by_domain` value ahead of `WB-D2` | Low-medium |
| Lifecycle-stage ratification treated as a rubber stamp | Low |

### Additional risks specific to this execution plan

| Risk | Severity | Mitigation |
|---|---|---|
| `WB-22`'s validator and the two project-level schemas (`WB-9`, `WB-15a`/`WB-15b`) have no assigned name or file location — an implementer could invent one inconsistently with existing `scripts/`/`core/` conventions. | Medium | Treat as an **engineering decision, not an organizational one** — follow the existing precedent (`validate_eads.py`, `check_governance_sync.py`, `check_governance_ids.py` under `scripts/`; Core-only files under `core/schema/`; project-state extensions likely adjacent to `PROJECT_STATE.json`, exact path still open) and record the choice explicitly when made, rather than silently assuming one. |
| `WB-24`'s "per-area review" could be skipped or compressed under schedule pressure, letting an unreviewed organizational decision flow into downstream schema/content work. | Medium | `WB-24` is listed as a hard gate before any consuming milestone in Section 8 — this plan does not permit `WB-9`-and-later work to treat an unreviewed decision as final. |
| A `WB-D2` resolution of "enumerate" could arrive after `WB-11a`/`WB-12a` are already drafted, creating pressure to retroactively bake enum assumptions into those files. | Low | `WB-11a`/`WB-12a`'s acceptance criteria (Section 8) explicitly require $ref-based (or equivalent) composition precisely so the enum's eventual arrival via `WB-14` requires no edit to `WB-11a`/`WB-12a` themselves. |

### Assumptions this plan makes explicit

- The committed assessment (`f852893`) is the final, approved statement of Workstream B's scope and dependencies; this plan does not second-guess its content, only sequences it.
- No new Section 14 item or Workstream B decision has emerged since the assessment was committed.
- `core/`, Revision 8, and the Workstream A plan remain unchanged at the time this plan is read (confirmed in Section 0 for the time of writing — **re-verify before execution begins**, since time may have passed).

### Unresolved questions (not organizational — left open deliberately, per the assessment's own Section 8)

- `change-classification.schema.json`'s full field shape beyond `gate_impact` is not reproduced anywhere in Revision 8's available text (assessment Section 8) — `WB-13`'s acceptance criteria can only be as precise as what Revision 8 actually specifies plus `WB-5`'s decision.
- The exact file location for the two project-level schemas remains an open question Revision 8 itself acknowledges as "named, not designed" — this plan surfaces it (Section 7, Section 10) rather than guessing.

---

## 11. Completion checklist

Workstream B is **not** complete until every item below is true. This checklist does not replace `WB-26`'s own acceptance criteria (Section 8) — it restates them as a single final gate.

- [ ] All nine organizational input register entries (Section 6) resolved and recorded, each traceable to a named decision-maker.
- [ ] `WB-1` through `WB-26` (28 total bullets, including the retirement note) all completed per Section 8's acceptance criteria — **no milestone skipped, none renumbered, `WB-11b`/`WB-12b` remain retired**.
- [ ] All new Core files present: `core/gates.yaml`, `core/artifacts.yaml`, `core/lifecycle.yaml`, `core/change-classification.yaml`; all validate against their schemas.
- [ ] `core/governance.yaml` contains exactly one new rule (`GOV-013`, with `EXC-001`), no existing rule altered.
- [ ] `core/manifest.yaml` updated per `WB-21`; `lifecycle_state` still `draft`.
- [ ] All new/modified JSON Schemas are valid; `authority-requirement.schema.json` and `governance-rule.schema.json` modified only if and exactly as `WB-1`/`WB-14` determined.
- [ ] Cross-file reference integrity confirmed (`WB-22`); `check_governance_ids.py` regression-passes (`WB-23`).
- [ ] Fidelity review (`WB-25`) confirms no invented value anywhere in the bundle.
- [ ] No file outside the Section 7 impact matrix was touched.
- [ ] No Runtime component was built; Workstream C was not started; `lifecycle_state` did not advance past `draft`.
- [ ] Nothing was committed or pushed as part of *this planning document's* own preparation (this plan is itself subject to the same "do not implement" boundary it describes for Workstream B).

---

## Appendix: Mapping to the committed assessment's structure

| This plan's section | Assessment section it operationalizes |
|---|---|
| Section 3 (decision summary) | Assessment Section 3 (seven decision areas, eleven decisions) |
| Section 4 (dependency overview) | Assessment Section 5 (decision dependency matrix, critical path) |
| Section 6 (organizational input register) | Assessment Section 6 (nine organizational questions) |
| Section 7 (file impact matrix) | Assessment Section 4 (Core implementation implications) |
| Section 8 (milestone plan) | Assessment Section 7 (recommended implementation sequence) |
| Section 10 (risks) | Assessment Section 8 (risks and open questions) |
