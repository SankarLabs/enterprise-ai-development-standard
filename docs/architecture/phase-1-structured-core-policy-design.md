# EADS v0.2 — Phase 1: Structured Core Policy Design

**Status:** Proposed design, revision 8 — one consistency correction resolving a Workstream B / Workstream C contradiction. Not implemented. No Core files, schemas, or implementation code exist yet.
**Scope:** Design only. Nothing in this document is active policy.
**Location rationale:** No root-level `docs/` directory existed before this file. `methodology/` is EADS's user-facing standard content; `project-starter/docs/` is adopter-template content. Neither is the right home for EADS's own internal architecture-design records, so this document introduces `docs/architecture/` as that home.

---

## Revision 1 summary

Eight structural issues, fixed without redesigning anything already approved: tier applicability restructured as a status map; artifact-based gate evidence de-duplicated to a single authoring point; the `AUTH-*` role registry replaced with abstract authority domains; `authority_model` renamed to an eligibility list (`supported_authority_models`); whole-file-only documentation generation extended with a section marker concept; `trust_tier` removed from the Core capability schema; `classification` split into `rule_type` + `human_approval_required`; a `lifecycle_state` field added to the manifest.

## Revision 2 summary

Five further corrections: `human_approval_required` had been folded too generally from the retired `conditional` rule-kind; `GOV-013`'s `authorized_by: project-owner` reintroduced exactly the role problem the `AUTH-*` removal fixed; the manifest's `lifecycle_state` conflated Core's own review state with a project's adoption of it; a single shared `applicability.condition` string couldn't represent per-tier variation; `supported_authority_models` was shown with only one example.

## Revision 3 summary

Seven corrections: `GOV-013`'s scope was corrected from `["G4"]` to a new `before-gate` dimension matching the rule's actual pre-G4 reach; valid combinations of `rule_type`/`human_approval_required`/`exceptions` were defined explicitly; `scope` was given a closed, five-dimension shape; tier-completeness was made mandatory; conditional resolutions were required to reference the Core version they were resolved against; the Phase 1 plan's dependency sequencing for `GOV-013` was corrected; the hybrid-approval explanation was corrected to avoid reading `local`/`external` as a three-way choice including "hybrid."

## Revision 4 summary

Four corrections: content-snapshot comparison replaced inconsistent version-number comparison for conditional-resolution staleness; per-status field constraints were defined for the full applicability enum; a four-layer exception-authorization lifecycle (Section 5.2.2) made clear that a Core-authored exception is not itself an authorization; fail-closed `before-gate` evaluation semantics were defined so no unverifiable gate state can silently lift a prohibition.

## Revision 5 summary

Three hardening corrections: content-snapshot comparison was given precise normalization rules, a two-step compatibility-gate-then-content-comparison procedure, a five-case decision table, and seven worked examples; exceptions were given stable `EXC-###` identifiers instead of array-position references; the Phase 1 implementation plan was reorganized into Workstreams A (unblocked), B (organization-dependent, each item tagged with its blocking Section 14 item), and C (integration and ratification).

---

## Revision 6 summary

Three narrow corrections, found on review of revision 5's own new mechanisms — none redesign anything, each either sharpens a definition or removes an unintended overreach.

| # | Issue found | Fix applied |
|---|---|---|
| 1 | `compatible_schema_versions` was reused for both Runtime-loadability and snapshot-comparison safety without stating whether listing a version there asserted one guarantee or both — leaving room to read mere parseability as sufficient for snapshot-comparison safety. | Section 5.1 now defines the field as asserting **both** guarantees simultaneously, a strictly stronger claim than loadability alone. Section 5.5.1 updated so list membership *is* the safety assertion outright, not an assumption layered on top of a separate loadability check. The human/engineering judgment required to make that assertion, and the fail-closed migration-needed outcome when it hasn't been made, are both preserved unchanged. |
| 2 | The five authority-domain values (Section 5.7) and the `STAGE-0`..`STAGE-8` lifecycle-stage IDs were presented in schema tables as if settled, even though Section 14 already lists the domain taxonomy (item 7) and the lifecycle-stage enumeration (item 4) as unresolved — and Workstream A's plan risked authoring them as fixed enums. | Section 5.7's `domain` field and the lifecycle-stage schema are now explicitly scoped, in both their field tables and in Workstream A (Section 15), to *structure only* — the specific values shown throughout this document are relabeled as illustrative candidates for legibility, not an approved enum. Final values remain gated on Section 14 items 7 and 4 respectively. |
| 3 | Sections 9 and 12 implied Phase 1's own Core validator could check a project-level authorization record's `exception_id` against Core's `EXC-###` IDs — but no project-level record schema has been designed, and Phase 1 builds no Runtime capable of reading project state at all, so this check cannot actually run in Phase 1. | Section 9 and 12 now separate **Core-internal reference integrity** (Phase 1 scope, fully self-contained and automatable today — including `EXC-###` uniqueness) from **cross-layer validation** of project-level records against Core (stated as a requirement the future Runtime must satisfy, fail-closed, not something this phase's validator performs or can perform). Workstream C's validation scope is stated as Core-internal only. |

**Unresolved after this revision:** all items from revisions 1–5 remain open (Section 14) — none of these three corrections resolved an organizational question; they tightened scope and definitions around mechanisms already introduced.

---

## Revision 7 summary

One narrowly scoped correction, found immediately after revision 6's own validation-boundary fix: revision 6 correctly separated Core-internal validation from cross-layer validation in principle, but three checks were left miscategorized as "Core-internal" in Section 12's table even though all three require reading a project-level resolution record that doesn't exist as a designed schema yet.

| # | Issue found | Fix applied |
|---|---|---|
| 1 | Section 12's "Core-internal validation" table included "conditional artifact entries with no recorded resolution," the "schema-compatibility gate" check, and "normalized, load-bearing-field content comparison" — all three require a project-level resolution record (Section 5.5.1), which Phase 1's Core validator has no access to and which has no designed schema at all (Section 14, item 8). | All three moved into a renamed, expanded **"Project-state validation — future Runtime responsibility (Phase 2+)"** group, alongside the exception-ID check already there. Section 9 and Section 15 updated to reference this corrected grouping consistently, with the minimum wording changes needed to stay aligned. |

**Preserved unchanged by this correction:** resolving `conditional` remains a project-level human decision, never inferred; the schema-compatibility gate must be established before any content comparison, per Section 5.1's revision 6 dual-guarantee definition of `compatible_schema_versions`; an unverified compatibility gate still yields `migration-needed`; changed content still yields `stale`; missing or unverifiable project-level data is never silently treated as passing. **Unresolved after this revision:** all items from revisions 1–6 remain open (Section 14) — this correction fixed a categorization error, not an organizational question.

---

## Revision 8 summary

One consistency correction. Section 15's Workstream B explicitly designs the project-level authorization-record and conditional-resolution-record schemas — but Sections 9 and 12 had, in places, attributed Phase 1's inability to run cross-layer checks to the project-level record schema "not existing," which directly contradicts Workstream B's own stated deliverable once that workstream completes.

| # | Issue found | Fix applied |
|---|---|---|
| 1 | Sections 9, 12, and 15 stated or implied that cross-layer checks (exception-ID resolution, conditional-resolution staleness) cannot run in Phase 1 *because the project-level record schema doesn't exist* — but Workstream B, itself part of Phase 1, is explicitly tasked with designing that schema, making the stated reason self-contradicting. | Reframed the true, non-contradictory blocker throughout: a **designed schema** (Workstream B's deliverable, within Phase 1) is not the same thing as a **Runtime** capable of loading an actual project record and comparing it against Core — and no workstream of Phase 1 builds that Runtime. Sections 9, 12, and 15 now consistently state: schema design belongs to Workstream B; Core-internal-only validation belongs to Workstream C; cross-layer execution belongs to Phase 2+ Runtime, regardless of whether the schema exists by then. |

**Unresolved after this revision:** all items from revisions 1–7 remain open (Section 14) — this correction fixed an internal contradiction, not an organizational question.

---

## 1. Executive summary

EADS v0.1 expresses its entire governance model as prose Markdown, read and interpreted by whichever agent happens to be operating. Phase 0 already found and fixed one consequence of this: the same rules were independently restated, with drifting wording, across `AGENT_GOVERNANCE.md`, `AGENTS.md`, and `SKILL.md`. That fix was manual and document-scoped — it does not generalize.

This document proposes **EADS Core** as the fix at the right altitude: a small set of versioned, schema-validated YAML files that become the single authored source for governance rules, lifecycle stages, approval gates, artifacts, and change classification. Markdown becomes *generated* from Core, not hand-authored. This is a **data model design**, not a build — nothing is implemented, nothing in this document is active policy, every example is illustrative.

Six revisions of review have consistently found two failure modes: Core quietly absorbing something project-specific, and a mechanism being introduced without precisely specifying its behavior at the edges — including, this time, the edge between "this document is proposing a schema shape" and "this document is accidentally asserting specific enum values as settled." Section 14 remains the list of organizational questions nobody has answered yet.

---

## 2. Design goals and non-goals

Unchanged from revision 4/5.

**Goals:** agent-independent and Runtime-independent policy data; versioned and schema-validated; one canonical source per concept; human-reviewable; capable of generating Markdown and agent instructions (Phase 2+); extensible without inventing machinery nobody needs yet; correctly scoped to standard-level policy only; precise about a rule's actual reach; fail-closed at every point of uncertainty.

**Non-goals:** not a workflow engine, doesn't execute anything, no database; no claim of enforcement from mere representation; no Runtime code or migrations in Phase 1; no project-specific configuration stored in Core; no executable scope or condition language; no automatic authorization inferred from the mere existence of a Core-defined exception; **no schema structure doubling as a de facto ratification of the illustrative values used to demonstrate it** (new emphasis, revision 6).

---

## 3. Proposed Core directory structure

Unchanged from revision 3.

```
core/
├── manifest.yaml
├── governance.yaml
├── lifecycle.yaml
├── gates.yaml
├── artifacts.yaml
├── change-classification.yaml
├── capabilities.yaml
├── evaluation.yaml
├── schema/
│   ├── manifest.schema.json
│   ├── governance-rule.schema.json
│   ├── scope.schema.json
│   ├── lifecycle-stage.schema.json
│   ├── approval-gate.schema.json
│   ├── evidence-requirement.schema.json
│   ├── authority-requirement.schema.json
│   ├── artifact.schema.json
│   ├── change-classification.schema.json
│   ├── capability.schema.json
│   └── evaluation-spec.schema.json
└── CHANGELOG.md
```

---

## 4. Canonical data format recommendation

Unchanged from revision 1. **YAML**, validated against JSON Schema, safe subset only.

---

## 5. Schema designs with examples

All examples are **illustrative only**, marked `# PROPOSED — not active policy`.

### 5.1 Core policy metadata (`manifest.yaml`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string (semver) | yes | |
| `policy_version` | string (semver) | yes | |
| `lifecycle_state` | enum: `draft \| reviewed \| ratified` | yes | Never "active." |
| `released_at` | string (ISO-8601 date) | yes | |
| `files` | list of strings | yes | |
| `compatible_schema_versions` | list of strings | yes | **Clarified in revision 6 — a stronger, combined guarantee, not two separate ones that merely happen to share a list.** Listing a prior `schema_version` here asserts *both*: (a) a Runtime may load files of that version without refusing, **and** (b) the load-bearing fields used in conditional-resolution snapshot comparison (`status`, `condition` — Section 5.5.1) retain their meaning across the gap to the current version. A schema version that merely still parses does **not** qualify for this list on that basis alone — parseability and semantic safety are different questions, and this field answers the harder one. The human authoring a new schema version must have deliberately considered both before adding anything here; if a version is loadable but was *not* evaluated for snapshot-comparison safety, it must be left off this list, even though a Runtime could technically still load it. If this coupling ever proves too coarse in practice (a genuine need to load a version while staying conservative only about snapshot comparison), splitting into two fields would be the natural minimal extension — not attempted now. |
| `notes` | string | no | |

### 5.2 Governance rule (`governance.yaml`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string, pattern `GOV-\d{3}` | yes | |
| `title` | string | yes | |
| `rule_type` | enum: `permitted \| prohibited \| obligation \| accountability` | yes | |
| `description` | string | yes | |
| `scope` | list of Scope objects | yes | Section 6.1. |
| `required_behavior` | string | conditional | |
| `prohibited_behavior` | string | conditional | |
| `human_approval_required` | boolean | no | Never `true` when `rule_type: prohibited`. |
| `exceptions` | list of Exception objects | no | Each carries a stable `id`. Valid only when `rule_type: prohibited`. |
| `enforcement_expectation` | string | no | |
| `references` | list of IDs | no | |
| `status` | enum: `active \| deprecated` | yes | |
| `superseded_by` | string (ID) | conditional | |

**Exception object shape:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string, pattern `EXC-\d{3}` | yes | Flat namespace across `governance.yaml`. |
| `condition` | string | yes | |
| `authorized_by_domain` | string, constrained to the domain taxonomy once ratified | yes | **Clarified in revision 6** — same candidate domain values as Section 5.7, illustrative only, not yet an approved enum. No new role, no new domain value introduced here. |

```yaml
# PROPOSED — not active policy — illustrative governance.yaml excerpt
rules:
  - id: GOV-001
    title: "No invented approvals"
    rule_type: prohibited
    description: >
      Never invent business facts, approvals, requirements, evidence, test
      results, compliance claims or stakeholder decisions.
    scope: [{ dimension: all-agents }]
    prohibited_behavior: "Fabricating any of the listed categories."
    status: active

  - id: GOV-006
    title: "Ask before installing dependencies or tools"
    rule_type: permitted
    description: "Agents may install dependencies or tools, but only after explicit human confirmation."
    scope: [{ dimension: all-agents }]
    human_approval_required: true
    status: active

  - id: GOV-013
    title: "Discovery spike exception to pre-G4 restriction"
    rule_type: prohibited
    description: >
      Do not create production code, schema migrations, infrastructure
      changes, dependency upgrades or generated application scaffolding
      before G4, unless authorized as a bounded discovery spike.
    scope:
      - { dimension: before-gate, reference: G4 }
    exceptions:
      - id: EXC-001
        condition: "Explicit scope, timebox, isolated branch/environment, no production impact, and a cleanup plan are all recorded."
        authorized_by_domain: general   # illustrative candidate value — see Section 5.7; not an approved enum member
    status: active
```

#### 5.2.1 Scope and exception mechanics

Unchanged from revision 3/4. `GOV-013`'s `scope` uses `before-gate` — see 6.1.1 for its fail-closed evaluation. No field on this rule carries `human_approval_required`: only the pre-authored `EXC-001` entry can create the discovery-spike carve-out.

#### 5.2.2 Exception authorization lifecycle

**The existence of `EXC-001` in Core is not itself an authorization to do anything.** It is a precondition, one of four distinct layers that must *all* be satisfied before a specific discovery spike is actually permitted:

| Layer | What it is | Where it lives | What it is NOT |
|---|---|---|---|
| 1. Core-authored exception definition | `EXC-001`, nested under `GOV-013` — states that an exception to this prohibition *can* exist, bounded by its `condition` text, requiring authority from whichever domain is ultimately ratified for this purpose (illustrated above as `general`). | Core (`governance.yaml`) | Not a grant. |
| 2. Project configuration: domain → identity mapping | A record, specific to one project, saying who or what group actually holds that domain's authority there. | Project configuration — not Core, not designed in this document (Section 14, item 8) | Not a decision about any particular spike. |
| 3. Human authorization of one specific instance | A named, authenticated individual — identified via layer 2's mapping — explicitly authorizing *this* discovery spike, citing `EXC-001` by its stable ID, with its own actual scope/timebox/branch/cleanup-plan matching layer 1's bounding `condition`. | Project-level record (schema not yet designed — Section 14, item 8) | Not automatic. Must be a real, attributable, per-instance act. |
| 4. Runtime verification | Before allowing the otherwise-prohibited action, a future Runtime (Phase 2+) checks that layer 3's authorization exists, cites a real `EXC-001`, was granted by someone layer 2 recognizes, and stays within layer 1's bounds. **This Runtime must reject any authorization citing a nonexistent exception ID, failing closed exactly as Section 6.1.1 requires for gate status** — this requirement is preserved unchanged by this revision even though Phase 1 does not build the Runtime that will satisfy it (Section 9, Section 12). | Runtime (not built in Phase 1) | Not optional once built. |

---

### 5.3 Lifecycle stage (`lifecycle.yaml`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string, pattern `STAGE-\d` | yes | **Clarified in revision 6:** this is the field's *structural* pattern only. The specific `STAGE-0`..`STAGE-8` values used in this document's examples mirror the numbering already in `LIFECYCLE.md` for legibility, but are not hereby asserted as the ratified, final ID set — confirming them is bundled with Section 14, item 4's broader, still-open question about canonical lifecycle-stage enumeration. |
| `name` | string | yes | |
| `description` | string | yes | |
| `artifact_refs` | list of artifact IDs | yes | |
| `exit_criteria` | string | yes | |
| `gate_ref` | string (gate ID) | no | |

```yaml
# PROPOSED — not active policy — illustrative lifecycle.yaml excerpt
stages:
  - id: STAGE-1
    name: Discover
    description: "Understand the business problem, current process, users, stakeholders, outcomes, constraints, existing systems and evidence."
    artifact_refs: [PROJECT_BRIEF, STAKEHOLDERS, CURRENT_STATE, OPEN_QUESTIONS, GLOSSARY]
    exit_criteria: "Business owner reviews the problem statement, scope boundary and discovery assumptions."
    gate_ref: G0
```

### 5.4 Approval gate (`gates.yaml`)

Unchanged in shape from revision 1. See Section 7 for `supported_authority_models`. `authority_requirement.domain` values are illustrative candidates per Section 5.7 — not yet an approved enum.

### 5.5 Artifact definition (`artifacts.yaml`)

Unchanged from revision 4/5 — tier completeness required; per-status field constraints (`condition` mandatory and non-empty only on `conditional`, forbidden otherwise) unchanged.

```yaml
# PROPOSED — not active policy — illustrative artifacts.yaml excerpt
artifacts:
  - id: PROJECT_BRIEF
    filename: PROJECT_BRIEF.md
    purpose: "Business problem, outcomes, scope and constraints."
    typical_owner: "Sponsor / product owner"
    gate_associations: [G0]
    applicability:
      by_tier:
        "1": { status: required }
        "2": { status: required }
        "3": { status: required }
    status: active

  - id: CURRENT_STATE
    filename: CURRENT_STATE.md
    purpose: "Existing process/system baseline."
    typical_owner: "Analyst / architect"
    gate_associations: [G0]
    applicability:
      by_tier:
        "1": { status: conditional, condition: "Required only if this Tier 1 utility replaces or wraps an existing script or manual process." }
        "2": { status: conditional, condition: "Required whenever an existing departmental system or process is being replaced or integrated with." }
        "3": { status: required }
    status: active
```

#### 5.5.1 Conditional resolution and its versioning

Resolving a `conditional` status remains a recorded, project-level human decision, never an automatic default. Content-snapshot comparison (not version-number comparison) determines staleness.

**Snapshots compare parsed, normalized structures — never raw YAML text.** Key ordering is ignored. String values are compared after trimming whitespace and normalizing line endings, but internal whitespace is never collapsed — a deliberately conservative choice that risks an occasional false "changed" over any risk of a false "unchanged." Comparison is scoped to load-bearing fields (`status`, `condition`; Section 14, item 14 flags this scope as a proposed minimal set).

**Schema compatibility is a separate, prior gate — and, per Section 5.1's clarified definition, it is not a loadability check that this comparison then separately trusts.** Before any content comparison:

- If the resolution's recorded `schema_version` equals the project's currently adopted one, proceed directly to content comparison.
- If it differs, comparison may proceed only if the current manifest's `compatible_schema_versions` includes the resolution's recorded `schema_version`. **Per Section 5.1, being listed there already is the safety assertion** — both loadable and semantically safe for this exact comparison — not a loadability allowlist that this step then additionally assumes is fine to reuse. There is no second, implicit safety assumption layered on top of list membership.
- If the recorded `schema_version` is **not** in that list, the resolution is **migration-needed** — content is never even compared, because nothing established the snapshot's fields still mean what they meant when recorded.

**The complete decision table:**

| Case | `schema_version` | Compatibility (per Section 5.1's stronger definition) | Normalized content | Result |
|---|---|---|---|---|
| A | same as current | n/a | equal | **Valid — unchanged.** |
| B | same as current | n/a | different | **Stale — content changed.** |
| C | different, listed in `compatible_schema_versions` | established (loadable *and* snapshot-safe) | equal | **Valid — backward-compatible schema change, content unaffected.** |
| D | different, listed | established | different | **Stale — content changed** despite the compatible schema change. |
| E | different, **not** listed | not established — regardless of whether the version happens to be loadable | never checked | **Migration-needed.** Fails closed before content is compared at all. |

Worked examples (formatting-only, key-order, real wording change, additive field under a declared-compatible change, policy-only bump with unchanged content, schema-only compatible change, schema change with unverified compatibility) are unchanged from revision 5 and are not repeated here for brevity; the mechanics above are identical, only the compatibility gate's meaning has been sharpened.

### 5.6 Evidence requirement (nested type)

Unchanged from revision 1.

### 5.7 Authority requirement (nested type)

| Field | Type | Required | Notes |
|---|---|---|---|
| `domain` | string, to become a constrained enum **once ratified** | yes | **Clarified in revision 6.** This document's examples use five illustrative candidate values — `business`, `technical`, `security`, `release-management`, `general` — chosen to demonstrate the schema's shape without inventing named organizational roles. **These are not an approved enum.** Workstream A (Section 15) may author this field's *type* — a constrained string — without asserting this specific value list as final. The permitted-values list is populated only once Section 14, item 7 is resolved. Used both on gates (5.4) and rule exceptions (5.2). |

**Open question, unchanged:** whether Core should enumerate domains at all, or require only "an authenticated, authority-appropriate decision" with no domain taxonomy. Section 14, item 7.

### 5.8 Change classification (`change-classification.yaml`)

Unchanged from revision 1.

### 5.9 Agent capability requirement (`capabilities.yaml`)

Unchanged from revision 1. Ships empty.

### 5.10 Evaluation specification (`evaluation.yaml`)

Unchanged from revision 1. Ships empty.

---

## 6. Governance rule representation

Unchanged from revision 3/4.

### 6.1 Scope representation

Unchanged — five closed dimensions, OR semantics. `gate`/`stage`/`agent-adapter`/`all-agents` are context-matches; only `before-gate` is a status-match. Multiple matching entries never combine.

#### 6.1.1 `before-gate` evaluation semantics — fail-closed

Unchanged.

| Gate X's actual state | Does `before-gate: X` match? |
|---|---|
| No recorded decision | **Matches.** |
| `pending` | **Matches.** |
| `rejected` | **Matches.** |
| `approved`, but verification returns anything other than a fresh `verified_match` | **Matches.** |
| `approved` **and** independently confirmed | **Does not match.** |

No state results in a silent bypass.

---

## 7. Approval gate representation

Unchanged. `local`/`external` are the two selectable authority sources; hybrid approval is the constant property that EADS keeps its own linked record under either, not a third selectable option. `authority_requirement.domain` values shown are illustrative candidates (Section 5.7), not an approved enum.

---

## 8. Artifact catalog design

Unchanged from revision 5. `artifacts.yaml`'s `gate_associations` is the only place the gate↔artifact relationship is authored; the derivation algorithm delegates staleness evaluation to Section 5.5.1's decision table.

---

## 9. Policy references and relationships

**Core-internal reference integrity — Phase 1 scope.** Every object type has a namespaced, stable ID: `GOV-###`, `STAGE-#`, `G#`, artifact filename-derived IDs, change-class names, `CAP-*`, `EVAL-*`, `EXC-###`. All cross-references **within Core** are by ID. This includes `EXC-###` uniqueness across `governance.yaml` and scope `reference` fields resolving to real gates/stages (`agent-adapter` references remain unvalidatable, since no adapter registry exists in Core). This check is fully self-contained — Core validating only against itself — and is squarely Phase 1's own validation strategy (Section 12).

**Cross-layer validation — explicitly NOT Phase 1 scope, in any workstream (corrected in revision 8).** A future project-level authorization record (Section 5.2.2, layer 3) will cite an `EXC-###` by ID. Checking that such a citation resolves to a real exception requires two separate things: a designed project-level record schema — which **Workstream B designs, within Phase 1** (Section 15) — and a Runtime component capable of reading both Core and project state together and comparing them, which **no workstream of Phase 1 builds**. A designed schema is not a Runtime: even once Workstream B has finished, Phase 1's own Core validator still has nothing to execute this check with. It is stated here as a **requirement the future Phase 2+ Runtime must satisfy** — reject any authorization citing a nonexistent exception, failing closed, consistent with Section 6.1.1's philosophy — not as something any part of Phase 1's validation strategy does or claims to do.

**The same is true, for the same reason, of conditional-resolution staleness checking (Section 5.5.1).** The schema-compatibility gate and the normalized content comparison both read a project-level resolution record — again, one Workstream B may design within Phase 1, but reading and comparing an actual recorded instance of it still requires the Phase 2+ Runtime that no workstream builds. Phase 1's Core validator has nothing to execute these checks with, schema designed or not.

```yaml
# PROPOSED — not active policy — illustrative broken reference, for validation-design purposes only
# (Core-internal — this one Phase 1 can actually check)
artifacts:
  - id: RISK_REGISTER
    gate_associations: [G9]   # fails validation — G9 does not exist

# A future project-level authorization record citing exception_id: EXC-099 would need to fail
# validation once a project-level schema and a Runtime exist to check it — not checkable by
# Phase 1's own Core validator, which has no such record to read.
```

---

## 10. Versioning and compatibility strategy

| | What it tracks | Bumped when |
|---|---|---|
| `schema_version` | The structural shape of the Core files | The shape changes |
| `policy_version` | The content | Any rule, gate, or artifact changes meaning, is added, or is deprecated |

**Core's own lifecycle, exactly three states:** `draft → reviewed → ratified`. **Project adoption** is separate, project-level, not designed here.

**Conditional-resolution staleness behavior:** see Section 5.5.1 for the complete decision table and Section 5.1 for `compatible_schema_versions`'s clarified, dual-guarantee meaning — not duplicated here.

**This repository's own governance is unchanged by any of this document** — EADS v0.1.0 remains this repository's adopted baseline until the already-approved v0.2 self-governance cutover (decision 12) is formally performed.

---

## 11. Generated documentation strategy

Unchanged from revision 1. Section-level `EADS:GENERATED:BEGIN/END` markers, generalizing the Phase 0 mechanism.

---

## 12. Validation strategy

Reorganized in revision 6 to separate validation that is genuinely Phase 1's own responsibility from a requirement stated for a future layer that doesn't exist yet. **Corrected in revision 7**: three checks were left miscategorized as Core-internal in revision 6, even though each one requires reading a project-level resolution record that has no designed schema. They are moved below into the project-state group, alongside the exception-ID check that was already correctly placed there.

### Core-internal validation (Phase 1 scope — self-contained, runs against Core files alone)

| Check | Automatable? | Notes |
|---|---|---|
| Schema validation, unique IDs, required fields, valid enums, reference integrity | Yes | |
| `rule_type: prohibited` never carries `human_approval_required: true` | Yes | |
| Every artifact's `by_tier` has all three tier entries; `condition` present only on `conditional` and non-empty there | Yes | |
| **`EXC-###` IDs are globally unique across `governance.yaml`** | Yes | Core-internal — no project-level data needed. |
| Scope `reference` fields resolve to real gates/stages | Yes | `agent-adapter` references remain unvalidatable (no registry exists). |
| `lifecycle_state` transitions only move `draft → reviewed → ratified` | Yes | |
| Exact-duplicate detection; generated-documentation drift | Yes | |

### Project-state validation — future Runtime responsibility (Phase 2+) (corrected grouping, revision 7)

None of these can run in Phase 1, **in any workstream** — corrected in revision 8, replacing the prior, self-contradicting claim that this was because no project-level record schema existed. Workstream B (Section 15) is explicitly tasked with designing those schemas within Phase 1; the actual, non-contradictory reason these checks cannot run in Phase 1 is that **loading an actual record and comparing it against Core requires a Runtime component, and no workstream builds one.** A designed schema is not a Runtime. They are stated here as requirements for the future Phase 2+ Runtime to satisfy once it exists — never as something Phase 1's own Core validator performs today, and never silently treated as passing merely because the project-level data they depend on is absent, unparseable, or unverifiable.

| Requirement | What it needs beyond Core | Behavior to preserve |
|---|---|---|
| **Conditional artifact entries with no recorded resolution are flagged, never silently resolved either way** | A project-level resolution record (schema: Workstream B deliverable) **and** a Runtime to load and read it | Resolving `conditional` remains a project-level **human** decision — Runtime surfaces the absence of one, it never infers a resolution. |
| **Schema-compatibility gate**: a resolution's recorded `schema_version` must equal the project's current one, or appear in the current manifest's `compatible_schema_versions` | The resolution record's recorded `schema_version` (schema: Workstream B deliverable) **and** the same Runtime | Per Section 5.1's revision 6 clarification, `compatible_schema_versions` asserts *both* Runtime loadability and snapshot-comparison semantic safety — list membership alone is the complete assertion. If the recorded version is not listed, the outcome is **`migration-needed`**, and content is never compared. |
| **Normalized, load-bearing-field content comparison** (Section 5.5.1) between a resolution's `content_snapshot` and the current Core entry | The resolution record's `content_snapshot` (schema: Workstream B deliverable) **and** the same Runtime | A changed result is **`stale`** — flagged for re-confirmation, never silently carried forward. |
| **A project-level authorization record's `exception_id` must resolve to a real `EXC-###`, rejecting it (fail-closed) if not** | The project-level authorization-record schema (Workstream B deliverable) **and** the same Runtime | Consistent with Section 6.1.1's fail-closed philosophy — an unresolvable citation is never treated as valid. |

**In every row above, the schema may be designed within Phase 1 (Workstream B) — the Runtime that reads and compares an actual record against Core is never built in any Phase 1 workstream.**

### Requires human judgment (neither Phase 1 nor any future automation resolves these alone)

| Check | Notes |
|---|---|
| Semantic fidelity, semantic conflict, inferred-mapping correctness, version-bump correctness | Unchanged. |
| Declaring a new `schema_version` eligible for `compatible_schema_versions` | Per Section 5.1, this requires evaluating *both* loadability and snapshot-comparison safety — not something the comparison logic derives on its own. |
| Whether the load-bearing-field scope (`status`, `condition`) is complete | Section 14, item 14. |
| Whether a `ratified` version should be adopted by a given project | Unchanged. |

---

## 13. Mapping existing v0.1/v0.2 content into the proposed Core model

Unchanged from revision 5.

---

## 14. Identified gaps, ambiguities, and design decisions requiring human approval

Items 1–13 carried forward; items 4 and 7 tightened in revision 6 to cross-reference the Workstream A scoping clarified this pass. None were resolved by this revision.

1. No authoritative gate↔artifact mapping exists anywhere today.
2. The shipped validator contradicts the stated tier-scaling principle; the schema can now express it precisely, but someone still has to decide the actual values.
3. `APPROVALS.md`/`PROJECT_STATE.json` aren't in the artifact catalog.
4. No canonical lifecycle-stage ID enumeration exists in `PROJECT_STATE.json` today. **Per revision 6, this also means Workstream A's `lifecycle-stage.schema.json` authoring is limited to structure — the `STAGE-0`..`STAGE-8` values shown in examples are not thereby the ratified, final ID set.**
5. The discovery-spike exception's structured fields should be confirmed against actual reviewer practice.
6. Change classification has no defined relationship to gates.
7. The authority-domain enum remains unsettled, including whether Core should enumerate domains at all. **Per revision 6, Workstream A may author the field's type shell but must not treat the five illustrative values shown in this document as pre-approved.**
8. Where project-specific authority-domain-to-identity mappings actually live is named, not designed.
9. The hybrid-approval evidence model is carried forward, not reopened.
10. `PROJECT_STATE.json` needs new fields (split version, project-adoption record, conditional-resolution records with `content_snapshot`) — none designed here.
11. The per-gate `supported_authority_models` eligibility lists are illustrative only.
12. The five scope dimensions are a proposed minimal set; `agent-adapter` scoping needs a registry that doesn't exist yet.
13. Content-snapshot equality is automatable but not provably complete proof that meaning hasn't changed.
14. The load-bearing-field scope used in content-snapshot comparison (currently `status`, `condition`) is a proposed minimal set.

---

## 15. Incremental implementation plan for Phase 1

Workstream structure unchanged from revision 5; scoping tightened within Workstream A and Workstream C per this revision's corrections 2 and 3.

### Workstream A — Unblocked foundation (can start immediately; no Section 14 dependency)

- Author JSON Schema documents for structures whose shape is already stable: `manifest.schema.json`, `governance-rule.schema.json` (including `scope` and the `EXC-*` exception shape), `evidence-requirement.schema.json`.
- **Author `authority-requirement.schema.json`'s field *type* only — a constrained string — without populating or asserting the five illustrative candidate values (business/technical/security/release-management/general) as an approved enum.** Final values are a Workstream B deliverable, gated on Section 14, item 7.
- **Author `lifecycle-stage.schema.json`'s field structure (id pattern, field names/types) only — without asserting `STAGE-0`..`STAGE-8` as the ratified, final ID set.** That determination is bundled with Section 14, item 4, and is also a Workstream B concern if it turns out to require more than copying existing `LIFECYCLE.md` numbering.
- Author `manifest.yaml` with `lifecycle_state: draft`.
- Migrate the domain-independent majority of `governance.yaml` — permissions, prohibitions with no `exceptions`, context-management, accountability.
- Validate that migrated content against the existing v0.1 `AGENT_GOVERNANCE.md` for fidelity (Section 13).
- Add `capabilities.yaml` and `evaluation.yaml` as empty-but-schema-valid files.

### Workstream B — Organization-dependent policy content

| Item | Blocked by |
|---|---|
| Resolve, then migrate, `gates.yaml`'s `authority_requirement.domain` values and `supported_authority_models` eligibility lists | Section 14, items 7, 11 |
| Populate `authority-requirement.schema.json`'s final enum values (Workstream A authored the type shell only) | Section 14, item 7 |
| Confirm (or revise) `lifecycle-stage.schema.json`'s `STAGE-0`..`STAGE-8` values as final (Workstream A authored the structure only) | Section 14, item 4 |
| Resolve, then migrate, `artifacts.yaml`'s `gate_associations` | Section 14, item 1 |
| Resolve, then migrate, `artifacts.yaml`'s `by_tier` status/condition values per tier | Section 14, item 2 |
| Resolve, then migrate, `change-classification.yaml`'s `gate_impact` field | Section 14, item 6 |
| Resolve, then migrate, `GOV-013`/`EXC-001`'s `authorized_by_domain` value | Section 14, item 7 |
| Design the `PROJECT_STATE.json` additions this document names but doesn't design: split version fields, project-adoption record, resolution records with `content_snapshot`, **and the project-level authorization-record schema that Section 9/12's cross-layer requirement depends on** | Section 14, items 3, 4, 8, 10 |

### Workstream C — Integration and completeness (after A and B are both done)

- Integrate all Core files together into one consistent set.
- Run the complete **Core-internal** schema and reference-integrity validation across the whole bundle (Section 9, Section 12's Core-internal table) — including `EXC-###` uniqueness and scope reference integrity. **This validation is Core-internal only.** **Corrected in revision 8:** Workstream B may well have already designed the project-level authorization-record and conditional-resolution-record schemas by this point (Section 14, item 8) — that design work is explicitly Workstream B's job, not a gap. What Workstream C does not do, regardless of whether those schemas exist, is **build or run the Runtime component that loads an actual project's records and compares them against Core.** A designed schema is not a Runtime. The exception-ID citation check and conditional-resolution staleness checking (schema-compatibility gate plus content comparison) both remain stated requirements for **Phase 2+ Runtime** (Section 9, Section 12's "Project-state validation" table) to execute once it exists — not a Workstream C deliverable, and not something Workstream C implements, simulates, or otherwise claims to perform.
- Perform a full semantic fidelity review against v0.1 (Section 13).
- Prepare for human review; on completion, `manifest.yaml` moves to `lifecycle_state: reviewed`, then — only once the entire bundle is confirmed complete and correct, never partially — `ratified`.

**Ratification remains a whole-bundle action.** **Explicitly deferred to Phase 2+:** the Policy Loader, schema-validation program, Structure/Gate evaluators, the Capability Registry, the Markdown generator, the project-adoption-record mechanism, the resolution-record storage and comparison logic, the agent-adapter registry, **and the Runtime component that performs the cross-layer exception-ID check named in Section 9/12.**

---

## Appendix: illustrative sample set recap

Every YAML/JSON fragment in this document is marked `# PROPOSED — not active policy` and exists only inside this file — no `core/` directory, schema file, project-config file, resolution record, exception registry, or generator was created on disk, in this revision or any prior one.
