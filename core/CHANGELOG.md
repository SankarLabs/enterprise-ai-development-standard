# Core Changelog

## 0.2.0 — 2026-11-23

- Workstream A (Phase 1: Structured Core Policy): authored the initial Core
  policy bundle at `lifecycle_state: draft`.
  - Added seven JSON Schemas under `core/schema/`: `manifest.schema.json`,
    `governance-rule.schema.json`, `evidence-requirement.schema.json`,
    `authority-requirement.schema.json`, `lifecycle-stage.schema.json`,
    `capability.schema.json`, `evaluation-spec.schema.json`.
  - Added `core/manifest.yaml` (`policy_version: 0.2.0`, `lifecycle_state: draft`).
  - Migrated all 28 rules from `methodology/AGENT_GOVERNANCE.md` into
    `core/governance.yaml` as `GOV-001`–`GOV-012`, `GOV-014`–`GOV-029`.
    `GOV-013` is reserved and intentionally not migrated; it depends on an
    unresolved authority-domain decision deferred to Workstream B.
  - Added empty, schema-valid placeholders `core/capabilities.yaml`
    (`capabilities: []`) and `core/evaluation.yaml` (`evaluation_specs: []`),
    to be populated in a later workstream.
  - Added `scripts/check_governance_ids.py` for cross-record GOV-###/EXC-###
    uniqueness checking, independent of per-object schema validation.
  - `lifecycle.yaml`, `gates.yaml`, `artifacts.yaml`, and
    `change-classification.yaml` are not yet authored (Workstream B).
