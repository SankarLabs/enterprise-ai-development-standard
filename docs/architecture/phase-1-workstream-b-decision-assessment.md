# EADS v0.2 — Phase 1, Workstream B: Decision & Dependency Assessment

**Status:** Assessment and planning only. Workstream B is **not authorized** and **not implemented**. No Workstream B schema, YAML, or `PROJECT_STATE.json` content has been created or modified. Nothing in this document is active policy, an approved schema, or a ratified organizational decision.
**Source of truth:** `docs/architecture/phase-1-structured-core-policy-design.md` (Revision 8, approved); `docs/architecture/phase-1-workstream-a-implementation-plan.md` (approved, as corrected); `core/` as committed at `4231a657fc8fde706c4febf7faf7f43eb7f17467`; `methodology/AGENT_GOVERNANCE.md`; `methodology/APPROVAL_GATES.md`; and, for grounding only, `methodology/LIFECYCLE.md`, `methodology/ARTIFACT_CATALOG.md`, `methodology/CHANGE_LIFECYCLE.md`, `project-starter/docs/PROJECT_STATE.json`.
**Scope:** Decision identification and dependency analysis for Workstream B only. Does not implement Workstream B, does not touch Workstream C (integration/ratification), does not touch Runtime (Phase 2+), and does not modify Revision 8, the Workstream A plan, or any file under `core/`.

---

## 0. Repository inspection (performed for this assessment)

- Branch: `feature/eads-v0.2`.
- HEAD: `4231a657fc8fde706c4febf7faf7f43eb7f17467` — `feat(eads): implement Phase 1 Workstream A structured Core policy`.
- Working tree: clean before this document was added.
- `main` and tag `v0.1.0`: both at `73eb3f75b3f39e02bf77dcf364bbaa72f2cc626e`; `git diff main v0.1.0` is empty — unchanged.

---

## 1. Executive summary

Workstream A delivered the **shape** of EADS Core: seven JSON Schemas and a draft policy bundle (`core/manifest.yaml`, `core/governance.yaml`, empty `core/capabilities.yaml`/`core/evaluation.yaml`) covering exactly the governance content that required no organizational decision. Fourteen gaps were deliberately left open by Revision 8, Section 14, and Workstream A touched none of them.

Workstream B's job is to close those gaps — but **it is not one job**. This assessment finds two largely independent decision tracks plus a small set of low-coupling schema-design items:

- **Track 1 — Authority & approval.** Whether Core enumerates authority domains at all, and if so with which values, is the single highest-leverage decision in Workstream B. It directly precedes two decisions that are themselves independent of each other and can proceed **in parallel** once it lands — the domain→identity mapping and `GOV-013`'s migration — and both of those, together with the domain decision itself, converge at a single join point: the project-level authorization-record schema. This fork-then-join shape is the **critical path**.
- **Track 2 — Artifacts, tiers, lifecycle, change classification.** Gate↔artifact associations, tier-specific artifact requirements, lifecycle-stage ID finalization, and change-classification→gate impact are four largely independent organizational decisions that do not depend on Track 1 and can proceed in parallel with it.
- **Low-coupling schema work.** The conditional-resolution-record schema and `PROJECT_STATE.json`'s structural additions (version-field split, project-adoption record) can be drafted at any time; they need real content from Track 2 to be *exercised*, not to be *designed*.

A second, more structural finding: **Workstream B is the first workstream that cannot remain strictly additive.** Workstream A's rollback section relied on "every change is strictly additive — new files under `core/`, nothing existing modified." At least one Workstream A file (`authority-requirement.schema.json`) will need an `enum` added to its `domain` field once Track 1 resolves, and `core/manifest.yaml` will need its `files` list and version fields updated once any Workstream B content file is added. Section 4 below details this.

This document makes **no organizational decision**. Where a decision has candidate options, they are labeled as proposals for human/organizational approval, not as choices this assessment is making.

---

## 2. Current architecture baseline

### 2.1 What Revision 8 already settled (not reopened here)

- Core directory structure, canonical YAML+JSON-Schema format (Section 3, 4).
- The complete `governance-rule.schema.json` shape, including `Scope` (five closed dimensions, OR semantics, `before-gate`'s fail-closed status-match) and `Exception` (stable `EXC-###`, flat namespace) — Section 5.2, 6.1, 6.1.1.
- The four-layer exception-authorization lifecycle (Core-authored exception → project domain/identity mapping → per-instance human authorization → Runtime verification) — Section 5.2.2.
- Content-snapshot comparison mechanics and the five-case staleness decision table — Section 5.5.1.
- The Core-internal / project-state / human-judgment three-way split of validation responsibility, and the Revision 8 correction that a *designed* project-level schema is not a *Runtime* — Section 9, 12.
- Core's own three-state lifecycle (`draft → reviewed → ratified`), separate from project adoption — Section 10.
- The Workstream A/B/C split itself, and the explicit Workstream B item list — Section 15.

### 2.2 What Workstream A actually built (commit `4231a65`)

| File | Content |
|---|---|
| `core/schema/manifest.schema.json` | Full schema — unused by Workstream B directly, but `core/manifest.yaml` (governed by it) will need edits (Section 4.3). |
| `core/schema/governance-rule.schema.json` | Full schema, including `Scope` and `Exception` `$defs`, exercised by all 28 rules. `Exception.authorized_by_domain` has **no `enum`** — deliberately. |
| `core/schema/evidence-requirement.schema.json` | Full schema (`description`, `kind` enum). **Unused by any Workstream A content** — prepared for `gates.yaml`. |
| `core/schema/authority-requirement.schema.json` | `domain` as an unconstrained, non-empty string. **No `enum`.** Unused by any Workstream A content — prepared for `gates.yaml` and for exception-bearing rules. |
| `core/schema/lifecycle-stage.schema.json` | `id` pattern `^STAGE-\d$` (structure only), no stage instances anywhere. Unused by any Workstream A content — prepared for `lifecycle.yaml`. |
| `core/schema/capability.schema.json`, `evaluation-spec.schema.json` | Full schemas, exercised only by empty arrays. |
| `core/manifest.yaml` | `lifecycle_state: draft`; `files: [governance.yaml, capabilities.yaml, evaluation.yaml]`; `compatible_schema_versions: []`. |
| `core/governance.yaml` | 28 rules, `GOV-001`–`GOV-012`, `GOV-014`–`GOV-029`. **`GOV-013` reserved, not present.** No rule carries `exceptions`. |
| `core/capabilities.yaml`, `core/evaluation.yaml` | Empty arrays. |
| `scripts/check_governance_ids.py` | Cross-record `GOV-###`/`EXC-###` uniqueness check, single-file scope (`core/governance.yaml` only). |

### 2.3 What already exists in v0.1 prose, relevant to Workstream B

Re-read directly for this assessment (not reconstructed from memory):

- **`methodology/APPROVAL_GATES.md`** — the complete G0–G5 gate model with required evidence and human decision per gate; the "Strict rules" section (source of `GOV-013`'s discovery-spike language); the six approval-record fields (`status`, `approved_by`, `approved_at`, `scope`, `evidence`, `notes`) that `PROJECT_STATE.json` already instantiates per gate. **No authority-domain taxonomy and no named roles appear anywhere in this file** — it only says "a human approver must be named and authorized under company policy."
- **`methodology/LIFECYCLE.md`** — Stage 0 through Stage 8, each with a name, description, artifact list, and exit criterion. This is the existing numbering the design doc's `STAGE-0`..`STAGE-8` examples mirror "for legibility" (Revision 6).
- **`methodology/ARTIFACT_CATALOG.md`** — a flat table of 23 artifacts with purpose and typical owner. **No tier column, no gate association column, no conditional-status logic exists here.** Confirms Section 14, item 1 and item 2 are genuinely unresolved, not merely unmigrated.
- **`methodology/CHANGE_LIFECYCLE.md`** — four change classes (Minor/Standard/Significant/Emergency) with no stated relationship to any gate. Confirms Section 14, item 6.
- **`project-starter/docs/PROJECT_STATE.json`** — `project.tier` is a free string (`"unclassified"`, no enum anywhere); `project.lifecycle_stage` is a free string (`"discovery"`) that does **not** use the `STAGE-#` ID scheme at all; `gates.*` records mirror `APPROVAL_GATES.md`'s six fields exactly; there is no `content_snapshot`, no conditional-resolution record, no project-level authorization record citing any `EXC-###`, and no `schema_version`/`policy_version` split.

This grounding matters for Section 3 below: for several items, Workstream B is not merely "structuring an existing prose decision" — the decision itself does not exist in any form yet, anywhere in this repository.

---

## 3. The seven decision areas

Each area distinguishes **approved architecture** (Revision 8, stated as settled) from **proposed recommendations** (this assessment's non-binding suggestions, requiring organizational sign-off). Decision owners are intentionally not assigned by this assessment; each requires designation by the relevant organization — consistent with Section 9's refusal to invent a role taxonomy. Section 6 identifies the decisions requiring organizational input.

### 3.1 Gate-to-artifact mappings — `WB-D1`

| | |
|---|---|
| **Revision 8 already defines** | `artifacts.yaml`'s `gate_associations` field is the *only* place the gate↔artifact relationship is authored (Section 8); the derivation algorithm for "what's needed by gate X" reads this field, not a separate mapping. The schema shape (tier-completeness required, `by_tier` status map) is fully specified (Section 5.5). |
| **Unresolved** | Which of the 23 cataloged artifacts associates with which of G0–G5. `ARTIFACT_CATALOG.md` has no such column today (Section 14, item 1: "No authoritative gate↔artifact mapping exists anywhere today"). |
| **Organizational input required** | A delivery/process owner must decide, per artifact, which gate(s) it feeds. This is a judgment call about the organization's actual review practice, not derivable from existing text. |
| **Can be designed independently** | The schema (`artifact.schema.json`) and the `gates.yaml`↔`artifacts.yaml` wiring convention can be fully designed without knowing the actual mapping values — Workstream A already proved this pattern (schema before content) for `authority-requirement` and `lifecycle-stage`. |
| **Dependencies** | None on other Workstream B decisions. Independent of the authority-domain track entirely. |
| **Risk of deciding incorrectly** | A missing gate association silently lets an artifact go unrequired at a gate where it should be reviewed; an over-broad one creates review burden with no corresponding value. Both are recoverable (Core is versioned; a later `policy_version` bump corrects it), but an incorrect mapping that ships as `ratified` could be treated as authoritative by a Phase 2+ Runtime before anyone notices the error. |
| **Recommended options (proposals only)** | (a) Derive a first-pass mapping mechanically from each artifact's position in `LIFECYCLE.md`'s stage list and that stage's `gate_ref`, then have a human reviewer confirm/adjust — lower effort, but inherits any existing gap between `LIFECYCLE.md` and actual practice. (b) Have gate owners (per `APPROVAL_GATES.md`'s "Human decision" column) each independently list the artifacts they require, then reconcile — higher effort, more likely to reflect real practice. Either way, the decision itself is organizational; this assessment does not pick one. |

### 3.2 Authority domains and approver groups — `WB-D2`, `WB-D3`, `WB-D4`

This area intentionally does **not** produce a role taxonomy. Revision 1 already removed the `AUTH-*` role registry in favor of abstract authority *domains*; Revision 8 treats "approver group" as an unresolved question about whether domains should be enumerated at all, not as an invitation to name roles. Three separable decisions live here.

**`WB-D2` — Should `authority_requirement.domain` / `Exception.authorized_by_domain` be a constrained enum, and if so, what are the values?**

| | |
|---|---|
| **Revision 8 already defines** | The field's *type* (constrained string) in both `authority-requirement.schema.json` and `governance-rule.schema.json`'s `Exception` `$def` — both authored in Workstream A with **no enum**. Five illustrative candidate values are shown throughout Revision 8 purely for legibility: `business`, `technical`, `security`, `release-management`, `general`. Revision 8 is explicit and repeated: **these are not an approved enum** (Section 5.7, 5.2, 6 revision-6 correction). |
| **Unresolved** | Section 14, item 7, explicitly poses the prior question: "whether Core should enumerate domains at all, or require only 'an authenticated, authority-appropriate decision' with no domain taxonomy." This is not merely "which values" — it is "enumerate or not" first. |
| **Organizational input required** | A genuine policy choice about how much structure to impose on "who may authorize this." No amount of re-reading existing methodology resolves it — `APPROVAL_GATES.md` deliberately avoids naming authority types beyond "a human approver... authorized under company policy." |
| **Can be designed independently** | The schema mechanics for *either* outcome (enum vs. unconstrained string with a documented authorization convention) are already fully specified by Workstream A's type-shell approach — no further schema engineering is needed to express either choice once chosen. |
| **Dependencies** | Blocks `WB-D3`, `WB-D4`, `WB-D8`, `WB-D9` (listed below and in Section 5's matrix). This is the single most-blocking decision in Workstream B. |
| **Risk of deciding incorrectly** | Too coarse an enum (e.g., only `business`/`technical`) may not actually distinguish who in the organization can authorize a security exception from who can authorize a release; too granular an enum re-introduces the named-role problem Revision 1 deliberately removed. Choosing "no enum" defers the problem to project-level convention with no Core-level check at all — consistent with Revision 8's stated alternative, but weaker as a structural guarantee. |
| **Recommended options (proposals only)** | (a) Adopt the five illustrative values as the ratified enum — lowest implementation effort, but risks mistaking "convenient for examples" for "organizationally correct." (b) Run a short structured review with whoever actually authorizes G0–G5 approvals today and `APPROVAL_GATES.md`'s "Strict rules" discovery-spike exceptions, and let *that* determine the value set — more effort, more likely correct. (c) No enum; `domain` remains a free, non-empty string, and "authority-appropriate" is established by project-level convention/documentation, never by Core — matches Section 14, item 7's named alternative directly. This assessment takes no position among (a)/(b)/(c). |

**`WB-D3` — Where and how does a project record which identity holds which domain's authority (exception-lifecycle layer 2)?**

| | |
|---|---|
| **Revision 8 already defines** | That this mapping is layer 2 of the four-layer exception-authorization lifecycle (Section 5.2.2), that it is project-specific, and that it is explicitly **not Core** and **not designed** in Revision 8 (Section 14, item 8: "named, not designed"). |
| **Unresolved** | Everything about its shape: file location, schema, whether it is per-project or per-organization, how it relates to `PROJECT_STATE.json`. |
| **Organizational input required** | Depends on how the organization actually manages authorization at the identity level (e.g., is this a CODEOWNERS-style mapping, a separate access-control system, a simple YAML list?) — outside EADS's own authority to decide unilaterally. |
| **Can be designed independently** | Only after `WB-D2` settles whether there even are domains to map identities to. If `WB-D2` resolves to "no enum," this decision changes shape entirely (mapping identities to an open-ended convention rather than a closed domain list). |
| **Dependencies** | Depends on `WB-D2`. Blocks `WB-D9` (the project-level authorization record needs to know what layer 2 looks like to reference it correctly). |
| **Risk of deciding incorrectly** | If this mapping is designed before `WB-D2` settles, it may need to be redesigned entirely rather than extended — wasted work, not a safety risk per se (nothing is enforced yet; Phase 1 builds no Runtime). |
| **Recommended options** | Not proposed in detail here — this decision's shape is downstream of `WB-D2` and premature to sketch before that lands. |

**`WB-D4` — Per-gate `supported_authority_models` eligibility lists (local/external)**

| | |
|---|---|
| **Revision 8 already defines** | `local`/`external` as the two selectable authority sources per gate; that "hybrid approval" is the constant property that EADS keeps its own linked record under either source, not a third selectable option (Section 7). The schema shape for `gates.yaml` is otherwise unchanged from Revision 1. |
| **Unresolved** | Section 14, item 11: "The per-gate `supported_authority_models` eligibility lists are illustrative only" — i.e., which gates accept `local`, which accept `external`, which accept both, has never been decided for any real gate. |
| **Organizational input required** | Whether, e.g., G5 (release authorization) may be satisfied by an external system of record (a change-management tool) versus requiring EADS's own local approval record, is a real operational policy question. |
| **Can be designed independently** | The `local`/`external` selectable-source mechanic itself needs no further design; only the per-gate value assignment is open. |
| **Dependencies** | None — gates G0–G5 already exist, fully identified in `methodology/APPROVAL_GATES.md`, independent of `WB-D1`'s artifact-association work; not strictly dependent on `WB-D2` either. `local`/`external` is a different axis (evidence *source*) from domain (*who*). |
| **Risk of deciding incorrectly** | Allowing `external` where only a trusted local record should suffice weakens the hybrid-approval guarantee Revision 8 preserves; disallowing `external` where the organization already has an authoritative external system creates duplicate record-keeping. |
| **Recommended options** | Not proposed in detail — this is a per-gate operational decision best made by whoever owns that gate's actual approval process today. |

### 3.3 Lifecycle-stage IDs and definitions — `WB-D5`

| | |
|---|---|
| **Revision 8 already defines** | `lifecycle-stage.schema.json`'s complete field structure (`id` pattern `^STAGE-\d$`, `name`, `description`, `artifact_refs`, `exit_criteria`, `gate_ref`) — authored in Workstream A. The illustrative `STAGE-0`..`STAGE-8` numbering mirrors `LIFECYCLE.md`'s existing numbering "for legibility," explicitly **not** asserted as ratified (Section 5.3, revision 6). |
| **Unresolved** | Section 14, item 4: "No canonical lifecycle-stage ID enumeration exists in `PROJECT_STATE.json` today." Confirmed directly in this assessment: `PROJECT_STATE.json`'s `lifecycle_stage` field holds `"discovery"` — a free string that does not even use the `STAGE-#` scheme, let alone a numeric ID. |
| **Organizational input required** | Minimal, relative to the other areas — `LIFECYCLE.md`'s nine stages (0–8) already have names, descriptions, artifact lists, and exit criteria written out in full prose. The main organizational act is *ratifying* this existing numbering as final, not inventing new content. |
| **Can be designed independently** | Largely yes. The `id` pattern already accepts single digits 0–9, so no schema change is anticipated here (unlike `WB-D2`'s `authority-requirement.schema.json`) — see Section 4.2. |
| **Dependencies** | None on other Workstream B decisions. Independent of the authority-domain track. Loosely feeds `WB-D1` (gate-artifact mapping, since `gate_ref` per stage is one input to that) and `WB-D6` (tier-specific artifact lists may reference stage-scoped artifact sets), but does not block them — Workstream A's existing illustrative numbering is already usable as a working draft for either. |
| **Risk of deciding incorrectly** | Lowest risk in this document: `LIFECYCLE.md`'s content already reflects considered design, and Revision 8 flags only *ratification*, not content invention, as outstanding. The main risk is treating this as a rubber stamp without checking whether `LIFECYCLE.md` has silently drifted from actual practice since it was written (Section 14, item 5 raises an analogous concern for the discovery-spike fields). |
| **Recommended options (proposals only)** | (a) Ratify `LIFECYCLE.md`'s Stage 0–8 numbering and content as `STAGE-0`..`STAGE-8` directly, with a light editorial pass only. (b) Treat this as an opportunity to re-validate the nine-stage model against current practice before ratifying — more effort, lower chance of ratifying stale content. This assessment does not choose between them. |

### 3.4 Tier-specific artifact requirements — `WB-D6`

| | |
|---|---|
| **Revision 8 already defines** | The complete `by_tier` status-map shape: three tier entries (`"1"`, `"2"`, `"3"`) each with `status: required \| conditional \| optional \| not_applicable` and a `condition` field mandatory and non-empty only when `status: conditional`, forbidden otherwise (Section 5.5). Tier-completeness (all three tiers present) is mandatory. |
| **Unresolved** | Section 14, item 2, stated plainly: "The shipped validator contradicts the stated tier-scaling principle; the schema can now express it precisely, but someone still has to decide the actual values." Confirmed in this assessment: `ARTIFACT_CATALOG.md` has no tier column at all, for any of its 23 artifacts. |
| **Organizational input required** | For every one of 23 artifacts, a required/conditional/optional/not-applicable judgment for each of three tiers — 69 individual status values, each potentially needing a `condition` string (only when `conditional`). This is the single largest *volume* of organizational decision-making in Workstream B, even though no single value is individually high-stakes. |
| **Can be designed independently** | The schema and validation logic (tier-completeness check, per-status field constraints) are already fully specified and require no further engineering, regardless of whether `WB-D6`'s values exist yet. |
| **Dependencies** | None on other Workstream B decisions. Independent of the authority-domain track. Benefits from `WB-D1` (gate associations) being decided around the same time, since both populate the same `artifacts.yaml` file, but neither strictly blocks the other. |
| **Risk of deciding incorrectly** | Under-requiring for Tier 3 (presumably the highest-risk/most-scrutinized tier) weakens governance exactly where it matters most; over-requiring for Tier 1 reproduces the "template-filling" anti-pattern `ARTIFACT_CATALOG.md` itself already warns against ("must not be fabricated merely to fill a template"). |
| **Recommended options (proposals only)** | (a) Start from the two worked examples already in Revision 8 (`PROJECT_BRIEF.md` required at all three tiers; `CURRENT_STATE.md` conditional at Tiers 1–2, required at Tier 3) and extend the same reasoning pattern to the remaining 21 artifacts. (b) Commission a dedicated review pass per tier, independent of the per-artifact pattern in Revision 8's examples. This assessment does not choose between them, and explicitly does not propose the 69 values itself. |

### 3.5 Change classification and `gate_impact` — `WB-D7`

| | |
|---|---|
| **Revision 8 already defines** | That `change-classification.yaml` exists as a Core file and that its schema (`change-classification.schema.json`) is "unchanged from revision 1" in general shape (Section 5.8) — but Revision 8 never specifies `gate_impact`'s own field shape in the schema tables reproduced in this document; it is referenced only as an unresolved relationship. |
| **Unresolved** | Section 14, item 6: "Change classification has no defined relationship to gates." Confirmed: `CHANGE_LIFECYCLE.md`'s four classes (Minor/Standard/Significant/Emergency) exist with no gate reference anywhere. |
| **Organizational input required** | Two layers of decision, not one: (i) what `gate_impact` even *means* structurally — does a Significant change re-trigger specific gates, require new approval scope, or something else — and (ii) once that's decided, which of the four classes trigger which effect. Layer (i) is itself a design question this assessment flags as open, not merely a values-filling exercise like `WB-D6`. |
| **Can be designed independently** | Only partially — unlike `WB-D1`/`WB-D5`/`WB-D6`, the *shape* of `gate_impact` is not yet settled by Revision 8, so schema design and the organizational decision are more entangled here than elsewhere. |
| **Dependencies** | None on other Workstream B decisions, but internally two-staged (shape, then values) in a way the other Track 2 items are not. |
| **Risk of deciding incorrectly** | `APPROVAL_GATES.md`'s own "Strict rules" state "Material changes invalidate affected approvals and require re-review" — if `gate_impact`'s shape cannot express which approvals a given change class invalidates, this existing rule has no structured representation and remains permanently prose-only, undermining the entire point of Core. |
| **Recommended options (proposals only)** | (a) Model `gate_impact` as, per class, a list of gate IDs whose approval is invalidated and must be re-reviewed — directly operationalizes the "material changes invalidate affected approvals" rule already in `APPROVAL_GATES.md`. (b) Model it as a severity/escalation flag only, leaving the re-review mechanics to Workstream C/Runtime. This assessment flags (a) as the more directly traceable option to existing v0.1 text, without asserting it as decided. |

### 3.6 `GOV-013` discovery-spike exception and authorization — `WB-D8`

| | |
|---|---|
| **Revision 8 already defines** | The complete worked example for `GOV-013` (Section 5.2), its `before-gate` scope dimension and fail-closed evaluation (Section 6.1.1), and the four-layer exception-authorization lifecycle that governs when it may actually apply (Section 5.2.2). The Workstream A plan independently confirms `GOV-013` is sourced from `methodology/APPROVAL_GATES.md`'s "Strict rules" (re-confirmed directly in this assessment: items 3–4, "No production code... before G4 unless separately authorized as a discovery spike," "A discovery spike must have explicit scope, timebox, isolated branch/environment, no production impact and a cleanup plan" — this is `EXC-001`'s `condition` text, already present almost verbatim in v0.1 prose). |
| **Unresolved** | Section 14, item 5: "The discovery-spike exception's structured fields should be confirmed against actual reviewer practice" — i.e., even though the *condition* text is already well-sourced, nobody has confirmed the structured fields match how reviewers actually evaluate a spike request today. Separately, `EXC-001.authorized_by_domain`'s actual value is blocked on `WB-D2`. |
| **Organizational input required** | Confirmation (not invention) of the condition fields against real reviewer practice, plus whichever domain value or non-enum convention `WB-D2` settles on. |
| **Can be designed independently** | The rule and exception *shape* need no further design — Revision 8's worked example is already essentially migration-ready once `WB-D2` lands. This is the one Workstream B item that is mostly "waiting," not "designing." |
| **Dependencies** | Directly blocked by `WB-D2` for the `authorized_by_domain` value. Not blocked by `WB-D3`/`WB-D4` (migrating the rule itself does not require the identity-mapping or eligibility-list decisions — those are needed only once someone actually tries to *use* the exception). |
| **Risk of deciding incorrectly** | This is the one rule in Core that creates a structured, pre-authored carve-out to a strict prohibition. Migrating it with an incorrect or premature `authorized_by_domain` value (e.g., guessing ahead of `WB-D2`) risks shipping a Core-ratified exception whose authorization path doesn't match whatever `WB-D2` eventually settles — forcing a `policy_version` bump to fix, which Revision 8's versioning strategy tolerates but which is avoidable by simply sequencing `WB-D2` first. |
| **Recommended options (proposals only)** | Sequence this strictly after `WB-D2`, and treat item 5's "confirm against actual reviewer practice" as a lightweight review step, not a redesign — the condition text is already substantively present in `APPROVAL_GATES.md`. No specific `authorized_by_domain` value is proposed here, since that would preempt `WB-D2`. |

### 3.7 Project-level authorization and approval-record requirements — `WB-D9`, `WB-D10`, `WB-D11`

**`WB-D9` — Project-level authorization record (exception-lifecycle layer 3)**

| | |
|---|---|
| **Revision 8 already defines** | That this record must cite `EXC-001` (or any future exception) by its stable ID, be attributable to a named, authenticated individual, and carry its own scope/timebox/branch/cleanup-plan matching the cited exception's `condition` (Section 5.2.2, layer 3). That checking this citation resolves to a real `EXC-###` is explicitly a **Phase 2+ Runtime requirement**, not something any Phase 1 workstream executes (Section 9, 12, corrected in revision 8 to remove the prior self-contradiction). |
| **Unresolved** | The schema itself — field names, types, file location — is explicitly named as a Workstream B deliverable (Section 15) but not designed in Revision 8. |
| **Organizational input required** | Depends on `WB-D2` (is there a domain to record?), `WB-D3` (what does the identity side look like?), and `WB-D8` (a real exception to cite) before the record's own fields can be finalized. |
| **Can be designed independently** | A draft skeleton (citing-exception-id, authorizing-identity, scope/timebox/branch/cleanup-plan fields) can be sketched now, mirroring Workstream A's own "author the type shell before the enum" pattern — but cannot be finalized before `WB-D2`, `WB-D3`, **and** `WB-D8` have all landed. |
| **Dependencies** | Requires all three of `WB-D2`, `WB-D3`, and `WB-D8` — this is the join point. `WB-D3` and `WB-D8` each depend only on `WB-D2` and do not depend on each other, so they can proceed in parallel once `WB-D2` lands; `WB-D9` cannot finalize until both have (Section 5's matrix). |
| **Risk of deciding incorrectly** | A schema designed before `WB-D2`/`WB-D3`/`WB-D8` land risks needing structural rework, not just a value change — e.g., if `WB-D2` resolves to "no enum," the record's domain-citation field becomes a free-text convention rather than an ID lookup, which is a shape change, not a value change. |
| **Recommended options** | Defer finalization until `WB-D2`, `WB-D3`, and `WB-D8` have all landed; a non-binding skeleton may be drafted earlier (Section 7, `WB-15a`) for discussion purposes only. |

**`WB-D10` — Conditional-resolution record schema (`content_snapshot`)**

| | |
|---|---|
| **Revision 8 already defines** | The complete comparison mechanics: parsed/normalized structural comparison (never raw text), the two-step compatibility-gate-then-content-comparison procedure, and the five-case decision table (Section 5.5.1) — all fully specified, nothing organizational left open about *how* comparison works. |
| **Unresolved** | Only the record's own schema (what fields hold the snapshot, the recorded `schema_version`, and the resolution decision) — named as a Workstream B deliverable (Section 15, Section 14 item 10) but not designed. |
| **Organizational input required** | Minimal — this is closer to pure schema engineering than any other item in this document, since Revision 8 already specifies the comparison algorithm in full. |
| **Can be designed independently** | Yes, essentially fully — this schema does not depend on `WB-D2` or any other Workstream B organizational decision. It becomes *exercisable* once `WB-D6` (tier-specific conditional statuses) produces real conditional entries to resolve, but its own design does not require waiting for that. |
| **Dependencies** | None blocking; loosely benefits from `WB-D6` existing first so a worked example is available, but can be designed in parallel. |
| **Risk of deciding incorrectly** | Getting the load-bearing-field scope wrong (Section 14, item 14 already flags `status`/`condition` as "a proposed minimal set," not a closed one) could under- or over-trigger staleness; this is a real but bounded risk, correctable by widening the compared-field set in a later schema revision. |
| **Recommended options** | Design this schema early, in parallel with Track 2, precisely because it has the lowest organizational coupling in this document — it is a good candidate for an early, independently reviewable Workstream B milestone (see Section 7). |

**`WB-D11` — `PROJECT_STATE.json` structural additions (version-field split, project-adoption record)**

| | |
|---|---|
| **Revision 8 already defines** | That `schema_version` and `policy_version` are tracked separately in Core's own manifest (Section 5.1, 10); that "project adoption" of a ratified Core bundle is a separate, project-level concept not designed in Revision 8 (Section 10). |
| **Unresolved** | Section 14, item 10, bundles several additions together: split version fields, a project-adoption record, and resolution records. The resolution-record portion is `WB-D10`/`WB-D9` above; the remaining piece is how `PROJECT_STATE.json` itself records *which* Core `policy_version` a given project has adopted. |
| **Organizational input required** | Low — this is primarily a bookkeeping/schema question about `PROJECT_STATE.json`'s own structure, not a policy judgment call. |
| **Can be designed independently** | Yes, fully — no dependency on the authority-domain track or on `WB-D1`/`WB-D5`/`WB-D6`/`WB-D7`. |
| **Dependencies** | None blocking. |
| **Risk of deciding incorrectly** | Low stakes; `PROJECT_STATE.json` is project-local and per-project, so an incorrect shape here does not propagate into Core itself and is cheaply revised. |
| **Recommended options** | Treat as a small, early, independently reviewable milestone, same rationale as `WB-D10`. |

---

## 4. Core implementation implications

Workstream B requires new schemas, and — this is the structurally significant finding of this assessment — **at least one modification to an existing Workstream A file**, breaking the strictly-additive invariant Workstream A relied on. Nothing below is implemented by this assessment; it is identified only.

### 4.1 New schemas Workstream B will require

| New schema | Governs | Connection to existing Workstream A files |
|---|---|---|
| `core/schema/approval-gate.schema.json` | `core/gates.yaml` | Consumes `core/schema/evidence-requirement.schema.json` and `core/schema/authority-requirement.schema.json` as nested types — **both already authored in Workstream A specifically in anticipation of this file** (both are currently unused by any Workstream A content). A governance rule's `scope: [{dimension: gate, reference: "G#"}]` (already a valid shape in `governance-rule.schema.json`) will, for the first time, be checkable against a real gate ID once this file and its content exist. |
| `core/schema/artifact.schema.json` | `core/artifacts.yaml` | Each artifact's `gate_associations` will reference IDs defined by `gates.yaml`/`approval-gate.schema.json` above. Each `lifecycle-stage.schema.json` stage's `artifact_refs` field (already structurally authored in Workstream A, currently with nothing to reference into) will, for the first time, be checkable against real artifact IDs. |
| `core/schema/change-classification.schema.json` | `core/change-classification.yaml` | Its `gate_impact` field (shape not yet settled — `WB-D7`) will reference gate IDs from `gates.yaml` once that shape is decided. No dependency on any other existing Workstream A schema. |
| A project-level authorization-record schema (name/location TBD — **not** under `core/schema/`, since Core is pure policy and this is project state, per Revision 8's non-goals) | A future `PROJECT_STATE.json` extension | Must cite `governance.yaml`'s `EXC-###` IDs (e.g., `EXC-001` once `GOV-013` is migrated) by stable ID — the first real consumer of that namespace outside Core itself. |
| A conditional-resolution-record schema (name/location TBD, same caveat) | A future `PROJECT_STATE.json` extension | References `core/manifest.yaml`'s `schema_version` and `compatible_schema_versions` (Section 5.1) directly — the first real consumer of that field's "dual guarantee" semantics outside Core itself. |

**Where the two project-level schemas belong is itself unresolved** (Section 14, item 8: "named, not designed" — this includes *location*, not only *shape*). This assessment does not propose a location; it flags the open question.

### 4.2 Existing Workstream A files: expected to need modification

| File | Why | Nature of the change |
|---|---|---|
| `core/schema/authority-requirement.schema.json` | Once `WB-D2` resolves to "enumerate," the `domain` field needs an `enum` keyword added — it currently has none, by design. If `WB-D2` resolves to "do not enumerate," **no change is needed here at all.** | Schema modification, conditional on `WB-D2`'s outcome. |
| `core/schema/governance-rule.schema.json` (`Exception.authorized_by_domain`) | The Workstream A plan explicitly states this field uses "identical constraint" to `authority-requirement.schema.json`'s `domain` — "this document does not define two different notions of domain." If `WB-D2` adds an enum to one, consistency pressure argues for the same enum here — **but this schema currently has no `$ref` to `authority-requirement.schema.json`; the two fields are independently defined and could drift.** Whether to converge them (e.g., via `$ref`) or keep them independently-but-identically defined is itself an open schema-design question this assessment surfaces, not one Revision 8 answers directly. | Schema modification or architectural refactor, conditional on `WB-D2` and a new design decision about field coupling. |
| `core/manifest.yaml` | Any new Workstream B content file (`gates.yaml`, `artifacts.yaml`, `lifecycle.yaml`, `change-classification.yaml`) must be added to `files`; `policy_version` must bump (new rules/content added — Section 10's bump rule); `compatible_schema_versions` may need an entry if any schema changes in a backward-compatible way (Section 5.1's dual-guarantee test applies). | Content modification to an already-committed Workstream A file — not additive. |
| `core/governance.yaml` | `GOV-013`/`EXC-001` is appended once `WB-D2`/`WB-D8` land. | Additive (a new rule appended) — does not modify any existing rule's content, but is the first change to this file since Workstream A. |

**No change is anticipated** to `manifest.schema.json`, `evidence-requirement.schema.json`, `capability.schema.json`, `evaluation-spec.schema.json`, or `lifecycle-stage.schema.json` — the last because its `id` pattern (`^STAGE-\d$`) already accepts any single digit 0–9 without modification once `WB-D5` ratifies specific values.

### 4.3 What this means for Workstream B's own rollback posture

Workstream A's plan could say "rollback is `rm -rf core/` or `git revert`, no existing file is ever touched." Workstream B cannot make the identical claim once `core/manifest.yaml` and potentially `core/schema/authority-requirement.schema.json` are modified in place. This does not block Workstream B — `git revert` still works — but it means Workstream B's own future implementation plan should state its rollback approach explicitly rather than inheriting Workstream A's "strictly additive" framing by default.

---

## 5. Decision dependency matrix

| Decision | Area | Depends on | Blocks | Can run in parallel with |
|---|---|---|---|---|
| `WB-D1` — gate↔artifact associations | 3.1 | None | Workstream C integration (Track 2 content) | `WB-D2`–`WB-D4`, `WB-D5`, `WB-D6`, `WB-D7`, `WB-D10`, `WB-D11` |
| `WB-D2` — authority-domain taxonomy (enumerate? values?) | 3.2 | None | `WB-D3`, `WB-D4`, `WB-D8`, `WB-D9` | `WB-D1`, `WB-D5`, `WB-D6`, `WB-D7`, `WB-D10`, `WB-D11` |
| `WB-D3` — domain→identity mapping location/shape | 3.2 | `WB-D2` | `WB-D9` | `WB-D1`, `WB-D4`–`WB-D8` (**including `WB-D8`** — both depend only on `WB-D2` and proceed independently of each other), `WB-D10`, `WB-D11` |
| `WB-D4` — `supported_authority_models` per gate | 3.2 | None — gates G0–G5 already exist, fully identified in `methodology/APPROVAL_GATES.md`, independent of `WB-D1`'s artifact-association work; not strictly dependent on `WB-D2` either (Section 3.2) | — | `WB-D1`, `WB-D2`, `WB-D3`, `WB-D5`–`WB-D8`, `WB-D10`, `WB-D11` |
| `WB-D5` — lifecycle-stage ID finalization | 3.3 | None | (loosely feeds `WB-D1`, `WB-D6`, non-blocking) | `WB-D1`–`WB-D4`, `WB-D6`–`WB-D8`, `WB-D10`, `WB-D11` |
| `WB-D6` — tier-specific artifact requirements (by_tier) | 3.4 | None | (exercises `WB-D10`'s schema; non-blocking) | `WB-D1`–`WB-D5`, `WB-D7`, `WB-D8`, `WB-D10`, `WB-D11` |
| `WB-D7` — change-classification `gate_impact` shape + values | 3.5 | None (internally two-staged) | — | `WB-D1`–`WB-D6`, `WB-D8`, `WB-D10`, `WB-D11` |
| `WB-D8` — `GOV-013`/`EXC-001` migration | 3.6 | `WB-D2` | `WB-D9` (joins with `WB-D3`; needs a real exception to cite) | `WB-D1`, `WB-D3`–`WB-D7` (**including `WB-D3`** — both depend only on `WB-D2` and proceed independently of each other), `WB-D10`, `WB-D11` |
| `WB-D9` — project-level authorization-record schema | 3.7 | `WB-D2`, `WB-D3`, `WB-D8` | Workstream C / Phase 2+ Runtime readiness | `WB-D10`, `WB-D11` (draft skeleton only, pre-dependencies) |
| `WB-D10` — conditional-resolution-record schema | 3.7 | None (design); `WB-D6` (to exercise) | — | Everything |
| `WB-D11` — `PROJECT_STATE.json` version/adoption fields | 3.7 | None | — | Everything |

**Critical path:** a fork-then-join, not a linear chain.

- `WB-D2` precedes `WB-D3`.
- `WB-D2` precedes `WB-D8`.
- `WB-D3` and `WB-D8` each depend only on `WB-D2` and do not depend on each other — **they can proceed in parallel once `WB-D2` lands.**
- `WB-D9` is the join point: it requires `WB-D2`, `WB-D3`, **and** `WB-D8` all to have landed before it can finalize.

This is the longest dependency path in Workstream B (two levels deep from `WB-D2` to `WB-D9`, with `WB-D3`/`WB-D8` as a parallel pair in between) and the only path that touches an organizational policy question (`WB-D2`) before any schema work on that path can finalize. Every other decision (`WB-D1`, `WB-D4`–`WB-D7`, `WB-D10`, `WB-D11`) is at most one level deep and does not depend on the authority-domain track at all.

**Practical implication:** Track 2 (artifacts/tiers/lifecycle/change-classification) could, in principle, be entirely resolved and even implemented before Track 1 (`WB-D2` and its dependents) produces a single answer. Sequencing Workstream B's actual implementation work around this split (Section 7) avoids making the slower, harder organizational decision (`WB-D2`) a bottleneck for the faster one.

---

## 6. Organizational questions to put in front of decision-makers

Listed once here, for a reviewer who wants the "what do you actually need to ask someone" list without re-reading Section 3 in full:

1. Should EADS Core enumerate authority domains at all, or require only "an authenticated, authority-appropriate decision" with no taxonomy? (`WB-D2`, Section 14 item 7)
2. If enumerated, what are the domain values — and who is actually authoritative to decide that, given no existing document names any role or domain today?
3. Where, organizationally, will the mapping from an authority domain to an actual authorized identity be recorded and maintained? (`WB-D3`, Section 14 item 8)
4. For each of G0–G5, should approval evidence be acceptable from an external system of record, EADS's own local record, or both? (`WB-D4`, Section 14 item 11)
5. For each of the 23 cataloged artifacts, which gate(s) actually require it today, in real practice — not in `LIFECYCLE.md`'s stage-to-artifact listing, which may or may not match? (`WB-D1`, Section 14 item 1)
6. For each of the 23 artifacts, at each of three tiers, is it required, conditionally required, optional, or not applicable — and for conditional entries, under what condition? (`WB-D6`, Section 14 item 2)
7. Should `LIFECYCLE.md`'s existing Stage 0–8 content simply be ratified as `STAGE-0`..`STAGE-8`, or re-validated against current practice first? (`WB-D5`, Section 14 item 4)
8. What should a change classification (Minor/Standard/Significant/Emergency) actually *do* to gate approvals — invalidate specific ones, flag for re-review, something else — and only then, which class does which? (`WB-D7`, Section 14 item 6)
9. Does the discovery-spike exception's structured representation (`GOV-013`/`EXC-001`) match how reviewers actually evaluate a spike request today? (Section 14 item 5)

None of these are answered by this assessment. All nine require a named organizational decision-maker, not an architecture document.

---

## 7. Recommended implementation sequence

Proposed, independently reviewable milestones, explicitly **not** including Runtime implementation or Workstream C ratification. Numbered `WB-1`.. for traceability; sequencing reflects Section 5's dependency matrix, not a claim that these are approved.

### Organizational decisions (no code, no schema — human decision-making only)

- **WB-1.** Resolve `WB-D2` (authority-domain taxonomy: enumerate or not; if so, values).
- **WB-2.** Resolve `WB-D1` (gate↔artifact associations) — independent of WB-1, may run concurrently.
- **WB-3.** Resolve `WB-D6` (tier-specific artifact requirements, all 23 artifacts × 3 tiers) — independent of WB-1, may run concurrently with WB-1/WB-2.
- **WB-4.** Resolve `WB-D5` (ratify or re-validate lifecycle-stage IDs) — independent, may run concurrently.
- **WB-5.** Resolve `WB-D7`'s shape question first (what does `gate_impact` structurally mean), then its values — independent, may run concurrently.
- **WB-6.** Resolve `WB-D3` (domain→identity mapping location/shape) — depends on WB-1.
- **WB-7.** Resolve `WB-D4` (per-gate `supported_authority_models`) — independent of both WB-1 and WB-2; gates G0–G5 already exist in `methodology/APPROVAL_GATES.md`, so this does not wait on either the authority-domain decision or the gate↔artifact association work, and may run concurrently with WB-1 through WB-6, WB-8.
- **WB-8.** Confirm `GOV-013`'s structured fields against actual reviewer practice (Section 14 item 5) — independent, may run concurrently with WB-1 through WB-7; does not require WB-1 to be resolved to perform the confirmation itself, only to finalize the `authorized_by_domain` value afterward.

### Schema design (engineering — gating varies by item: drafting a schema's *structure* from already-approved Revision 8 shape is not the same step as *finalizing* it against organizationally-decided content, and the two are separated below wherever Revision 8 already settles the structure)

- **WB-9.** Draft the conditional-resolution-record schema (`WB-D10`) — no organizational prerequisite; may start immediately, in parallel with WB-1.
- **WB-10.** Draft `PROJECT_STATE.json`'s version-split/project-adoption additions (`WB-D11`) — no organizational prerequisite; may start immediately.
- **WB-11a.** Draft `approval-gate.schema.json`'s structure now — no organizational prerequisite. Revision 8, Section 5.4, states this schema's shape is "unchanged in shape from revision 1," and it consumes `evidence-requirement.schema.json` and `authority-requirement.schema.json` as nested types, both already authored in Workstream A specifically in anticipation of this file (Section 4.1) — nothing about drafting the structure itself requires WB-1, WB-7, or WB-14 to have landed.
- **WB-12a.** Draft `artifact.schema.json`'s structure now — no organizational prerequisite. Revision 8, Section 5.5, already fully specifies the `by_tier` status-map shape (tier-completeness required; `condition` mandatory only on `conditional`) — nothing about drafting the structure itself requires WB-2 or WB-3 to have landed.
- **WB-13.** Author `change-classification.schema.json`, gated on WB-5 — unlike WB-11/WB-12, `gate_impact`'s own *shape* is not yet settled by Revision 8 (Section 3.5), so schema drafting and the organizational decision cannot be separated here; the shape question must resolve first.
- **WB-14.** Modify `authority-requirement.schema.json` to add the `domain` enum **only if** WB-1 resolved to "enumerate" — and resolve the `governance-rule.schema.json` `Exception.authorized_by_domain` convergence question (Section 4.2) explicitly, one way or the other, as its own reviewable decision rather than an incidental side effect.
- **`WB-11/12` retirement note.** `WB-11a` and `WB-12a` produce the complete schemas from structures already settled by Revision 8. `WB-14`'s later change to `authority-requirement.schema.json` should flow into `approval-gate.schema.json` through a shared `$ref` to that nested type, if that is the composition specified by Revision 8 — confirm that reference-based composition when drafting `WB-11a`; if the approved contract does not use `$ref`, resolve the nested-schema composition within `WB-11a` rather than assuming an automatic update. Similarly, `WB-2`/`WB-3` determine `artifact.schema.json`'s content *values*, not its already-defined *structure*. Therefore, the separate `WB-11b`/`WB-12b` schema-finalization milestones from earlier revisions of this assessment are **retired**. Actual YAML-to-schema validation for both files is performed after content creation, under `WB-22`.
- **WB-15a.** Sketch a non-binding skeleton of the project-level authorization-record schema (`WB-D9`) now, for discussion purposes only — no organizational prerequisite, mirroring Workstream A's own "author the type shell before the enum" pattern (Section 3.7's "Can be designed independently" row).

### Policy data migration (content authoring, each gated on its schema existing and its organizational decision landing)

- **WB-16.** Migrate `GOV-013`/`EXC-001` into `core/governance.yaml`, gated on WB-1 and WB-8.
- **WB-15b.** Finalize the project-level authorization-record schema, gated on WB-1, WB-6, and WB-16 — all three must land first, since the record must cite a real domain convention, a real identity-mapping shape, and a real exception ID; placed here, after WB-16, since WB-16 is one of its three dependencies.
- **WB-17.** Author `core/lifecycle.yaml` content, gated on WB-4 and (schema already exists from Workstream A, no new schema milestone needed).
- **WB-18.** Author `core/gates.yaml` content, gated on **WB-1, WB-7, WB-11a, and WB-14**. `WB-11a` supplies the complete schema; `WB-1`/`WB-7`/`WB-14` supply the approved authority-domain and per-gate authority-model decisions needed for the gate content.
- **WB-19.** Author `core/artifacts.yaml` content, gated on **WB-2, WB-3, WB-12a, WB-17, and WB-18**. `WB-12a` supplies the complete artifact schema; `WB-2`/`WB-3` supply gate associations and tier requirements; `WB-17` and `WB-18` supply the stage and gate IDs needed by `artifact_refs` and `gate_associations`.
- **WB-20.** Author `core/change-classification.yaml` content, gated on WB-13 and WB-18 (for `gate_impact` to reference real gate IDs).
- **WB-21.** Update `core/manifest.yaml`'s `files` list, `policy_version`, and `compatible_schema_versions` to reflect everything added above (Section 4.2) — this is its own reviewable milestone, not a silent side effect of any single file's migration.

### Cross-record validation (extending Workstream A's validation pattern to the larger bundle)

- **WB-22.** Extend or add Core-internal validation after all relevant content files have been authored: **(a)** validate every Core YAML file against its corresponding JSON Schema, including `manifest.yaml`, `governance.yaml`, `capabilities.yaml`, `evaluation.yaml`, `gates.yaml` (against `approval-gate.schema.json`), `artifacts.yaml` (against `artifact.schema.json`), `lifecycle.yaml` (against `lifecycle-stage.schema.json`), and `change-classification.yaml` (against `change-classification.schema.json`); and **(b)** check cross-file reference integrity: governance-rule `scope.reference` fields resolve to real gate/stage IDs; artifact `gate_associations` resolve to real gate IDs; and stage `artifact_refs` resolve to real artifact IDs. This is Core-internal and requires no Runtime, exactly as `check_governance_ids.py` already does for `GOV-###`/`EXC-###`.
- **WB-23.** Confirm `EXC-###` uniqueness still holds once `EXC-001` is added (re-run the existing `check_governance_ids.py` against the updated file — no new tooling needed for this specific check).

### Human review (mirroring Workstream A's checkpoint pattern)

- **WB-24.** Per-area review after each organizational decision (WB-1 through WB-8) lands, before any schema or content work consuming it begins — mirroring Workstream A's "after M1–M7, before M9" checkpoint pattern.
- **WB-25.** Fidelity review: confirm every migrated value (gate associations, tier requirements, stage definitions, change-impact mapping, `GOV-013`'s fields) traces to its organizational decision record, with no invented value — mirroring Workstream A's M13.
- **WB-26.** Full Workstream B acceptance pass: **(1)** all JSON Schema documents are syntactically valid and pass schema validation; **(2)** every Core YAML file validates against its corresponding schema; **(3)** all cross-record checks (`WB-22`, `WB-23`) pass; `core/manifest.yaml.lifecycle_state` remains `draft` (ratification is Workstream C, not in scope here); and no file outside the planned Workstream B set was touched.

**Explicitly excluded from this sequence, by the user's instruction and by Revision 8's own workstream boundaries:** any Runtime component (Phase 2+ only); Workstream C's integration pass and the `draft → reviewed → ratified` transition (Workstream C only, after Workstream B is fully complete).

---

## 8. Risks and open questions (consolidated)

| Risk | Where discussed | Severity if ignored |
|---|---|---|
| `WB-D2` decided too late or inconsistently, forcing rework of `WB-D3`, `WB-D8`, `WB-D9` | Section 3.2, 5 | High — longest dependency path in Workstream B (fork at `WB-D2` into parallel `WB-D3`/`WB-D8`, join at `WB-D9`) |
| Workstream B silently breaks the "strictly additive" invariant without anyone noticing `core/manifest.yaml` and possibly `authority-requirement.schema.json` need modification | Section 4 | Medium — not a safety issue, but an unstated scope/rollback-posture change from Workstream A's framing |
| `Exception.authorized_by_domain` and `authority-requirement.domain` drift into two differently-constrained notions of "domain" | Section 4.2 | Medium — undermines the Workstream A plan's own stated intent that they are "identical constraints" |
| Tier-specific requirements (`WB-D6`) filled in as a template-completion exercise rather than genuine per-artifact judgment | Section 3.4 | Medium — directly contradicts `ARTIFACT_CATALOG.md`'s own stated document-quality rule against fabricating content to fill a template |
| `gate_impact`'s shape question (`WB-D7`) treated as already-settled when it is not | Section 3.5 | Medium — risks building a schema that cannot express `APPROVAL_GATES.md`'s own "material changes invalidate affected approvals" rule |
| `GOV-013` migrated with a guessed `authorized_by_domain` value ahead of `WB-D2` | Section 3.6 | Low-medium — recoverable via a `policy_version` bump, but avoidable entirely by correct sequencing |
| Lifecycle-stage ratification (`WB-D5`) treated as a rubber stamp when `LIFECYCLE.md` may have drifted from practice | Section 3.3 | Low — lowest-risk item in this document, but not zero |

**Open questions this assessment could not resolve from the available sources** (distinct from the organizational questions in Section 6, which are decisions *for* humans — these are gaps in the source material itself):

- Revision 8 names `change-classification.schema.json` as "unchanged from revision 1" but no prior-revision text describing its full field shape is reproduced anywhere in the current document — only `gate_impact`'s *existence* is implied, not its shape. This assessment treats `gate_impact`'s shape as unresolved (`WB-D7`) rather than assuming a shape not actually specified anywhere available.
- The exact file location for the two project-level schemas (`WB-D9`, `WB-D10`) is acknowledged as unresolved by Revision 8 itself (Section 14, item 8's "named, not designed" language) — this assessment does not propose one.

---

## 9. Explicit scope exclusions

This assessment does **not**:

- Implement any Workstream B schema, YAML, or `PROJECT_STATE.json` content.
- Modify any file under `core/`, `methodology/`, or either approved architecture document.
- Decide any of the nine organizational questions in Section 6.
- Invent authority-domain values, lifecycle-stage IDs, tier values, approver-group names, or any other organizational decision — including declining to invent a universal role taxonomy, consistent with Revision 1's removal of `AUTH-*` and Revision 8's repeated "not an approved enum" framing.
- Propose, design, or implement any Runtime, agent-adapter, or project-state-execution component (Phase 2+, out of scope for all of Phase 1).
- Propose or perform Workstream C's integration pass or the `draft → reviewed → ratified` transition.
- Commit, push, or otherwise persist any change beyond this one new document.

---

## Appendix: Section 14 item → decision area traceability

| Section 14 item | Decision(s) in this assessment |
|---|---|
| 1 (gate↔artifact mapping) | `WB-D1` |
| 2 (tier-scaling values) | `WB-D6` |
| 3 (`PROJECT_STATE.json`/`APPROVALS.md` not in artifact catalog) | Noted in Section 2.3; not independently decision-tracked — resolved as a byproduct of `WB-D1`/`WB-D11` |
| 4 (lifecycle-stage ID enumeration) | `WB-D5` |
| 5 (discovery-spike fields vs. actual practice) | `WB-D8` |
| 6 (change classification ↔ gates) | `WB-D7` |
| 7 (authority-domain enum) | `WB-D2` |
| 8 (domain→identity mapping location; project-level authorization-record schema) | `WB-D3`, `WB-D9` |
| 9 (hybrid-approval model) | Not reopened — carried forward as settled per Revision 8 |
| 10 (`PROJECT_STATE.json` new fields: version split, adoption record, resolution records) | `WB-D10`, `WB-D11` |
| 11 (`supported_authority_models` eligibility lists) | `WB-D4` |
| 12 (self-governance cutover) | Not a Workstream B item — Revision 8 Section 10 states this repository's own governance is unaffected until a separately-performed cutover |
| 13 (content-snapshot equality completeness) | Not reopened — settled mechanics per Revision 8, Section 5.5.1 |
| 14 (load-bearing-field scope for snapshot comparison) | Noted in `WB-D10`'s risk entry; not a separate decision in this assessment, since Revision 8 already names `status`/`condition` as the working minimal set and this assessment does not propose expanding it |
