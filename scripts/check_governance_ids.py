#!/usr/bin/env python3
"""Check cross-record ID uniqueness in an EADS Core governance.yaml file.

Cross-record integrity validation, distinct from JSON Schema validation
(Phase 1 Structured Core Policy Design, Revision 8; Workstream A Implementation
Plan, Revision 8, Section 5 point 5). Schema validation confirms each
individual GOV-### / EXC-### string is well-formed; it does not confirm
that no two objects in the document share the same id. This script performs
that second, separate check.

This is a meta-repo tooling script, not Core data and not Runtime
functionality: it reads no project state, performs no enforcement, and
makes no policy decision.

Usage:
    python3 scripts/check_governance_ids.py <path-to-governance-yaml>
        Checks a real governance.yaml file for duplicate GOV-### rule ids
        and duplicate EXC-### exception ids (a flat namespace across the
        whole document, not scoped per rule). Requires PyYAML.

    python3 scripts/check_governance_ids.py --self-test
        Runs three embedded tests against hand-built fixtures: a positive
        case, and two negative cases (T5: duplicate GOV-### id; T6: duplicate
        EXC-### id across two different parent rules). Each test validates
        its fixture against core/schema/governance-rule.schema.json first,
        then runs find_duplicates() -- proving by construction that schema
        validation and cross-record validation are independent checks.
        Requires the Python jsonschema package. Does not require PyYAML,
        since self-test fixtures are built as Python dicts, not loaded
        from a YAML file.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def find_duplicates(doc: dict) -> dict:
    """Pure function: find duplicate GOV-### and EXC-### ids in a parsed
    governance document. No file I/O, no project state."""
    rule_ids = [r["id"] for r in doc.get("rules", [])]
    duplicate_gov_ids = sorted({i for i in rule_ids if rule_ids.count(i) > 1})

    # EXC-### is a flat namespace across the WHOLE document (Revision 8,
    # Section 9) -- collected across every rule's exceptions combined,
    # never scoped per-rule.
    exception_ids = [
        e["id"]
        for r in doc.get("rules", [])
        for e in r.get("exceptions", [])
    ]
    duplicate_exc_ids = sorted({i for i in exception_ids if exception_ids.count(i) > 1})

    return {"duplicate_gov_ids": duplicate_gov_ids, "duplicate_exc_ids": duplicate_exc_ids}


def check_file(path: Path) -> int:
    import yaml  # lazy import: only this code path needs PyYAML

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    result = find_duplicates(doc)

    if not result["duplicate_gov_ids"] and not result["duplicate_exc_ids"]:
        rule_count = len(doc.get("rules", []))
        exc_count = sum(len(r.get("exceptions", [])) for r in doc.get("rules", []))
        print(f"OK: {rule_count} unique GOV-### ids, {exc_count} unique EXC-### ids")
        return 0

    for gov_id in result["duplicate_gov_ids"]:
        count = [r["id"] for r in doc.get("rules", [])].count(gov_id)
        print(f"DUPLICATE GOV-### id: {gov_id} (appears {count} times)")
    for exc_id in result["duplicate_exc_ids"]:
        all_exc = [e["id"] for r in doc.get("rules", []) for e in r.get("exceptions", [])]
        count = all_exc.count(exc_id)
        print(f"DUPLICATE EXC-### id: {exc_id} (appears {count} times)")
    return 1


# --- Embedded self-tests (Section 9 of the Workstream A Implementation Plan) ---

def _governance_schema() -> dict:
    schema_path = Path(__file__).resolve().parent.parent / "core" / "schema" / "governance-rule.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _assert_schema_valid(doc: dict) -> None:
    from jsonschema import Draft202012Validator
    Draft202012Validator(_governance_schema()).validate(doc)  # raises on failure


def test_valid_document_has_no_duplicates() -> None:
    doc = {
        "rules": [
            {
                "id": "GOV-001",
                "title": "Read project files and approved documentation",
                "rule_type": "permitted",
                "description": "Agents may read project files and approved documentation.",
                "scope": [{"dimension": "all-agents"}],
                "status": "active",
            },
            {
                "id": "GOV-002",
                "title": "Example prohibition with an exception",
                "rule_type": "prohibited",
                "description": "Example only, for schema-fixture purposes.",
                "scope": [{"dimension": "all-agents"}],
                "prohibited_behavior": "Example prohibited behavior text.",
                "exceptions": [{"id": "EXC-001", "condition": "Example condition text.", "authorized_by_domain": "general"}],
                "status": "active",
            },
            {
                "id": "GOV-003",
                "title": "A second example prohibition with a different exception",
                "rule_type": "prohibited",
                "description": "Example only, for schema-fixture purposes.",
                "scope": [{"dimension": "all-agents"}],
                "prohibited_behavior": "Example prohibited behavior text.",
                "exceptions": [{"id": "EXC-002", "condition": "Example condition text.", "authorized_by_domain": "general"}],
                "status": "active",
            },
        ]
    }
    _assert_schema_valid(doc)  # step 1: schema-valid
    result = find_duplicates(doc)
    assert result == {"duplicate_gov_ids": [], "duplicate_exc_ids": []}, result  # step 2: no duplicates


def test_T5_duplicate_gov_id_is_detected() -> None:
    rule = {
        "title": "Duplicate-id fixture rule",
        "rule_type": "permitted",
        "description": "Example only, for schema-fixture purposes.",
        "scope": [{"dimension": "all-agents"}],
        "status": "active",
    }
    doc = {"rules": [{"id": "GOV-005", **rule}, {"id": "GOV-005", **rule}]}  # each rule individually well-formed
    _assert_schema_valid(doc)  # step 1: schema-valid despite the duplicate
    result = find_duplicates(doc)
    assert result["duplicate_gov_ids"] == ["GOV-005"], result  # step 2: duplication caught here


def test_T6_duplicate_exc_id_across_different_parent_rules_is_detected() -> None:
    def rule_with_exception(gov_id: str, exc_id: str) -> dict:
        return {
            "id": gov_id,
            "title": "Duplicate-exception-id fixture rule",
            "rule_type": "prohibited",
            "description": "Example only, for schema-fixture purposes.",
            "scope": [{"dimension": "all-agents"}],
            "prohibited_behavior": "Example prohibited behavior text.",
            "exceptions": [{"id": exc_id, "condition": "Example condition text.", "authorized_by_domain": "general"}],
            "status": "active",
        }

    doc = {"rules": [rule_with_exception("GOV-014", "EXC-001"), rule_with_exception("GOV-015", "EXC-001")]}
    _assert_schema_valid(doc)  # step 1: schema-valid despite the duplicate
    result = find_duplicates(doc)
    assert result["duplicate_exc_ids"] == ["EXC-001"], result  # step 2: duplication caught here


def run_self_test() -> int:
    tests = [
        test_valid_document_has_no_duplicates,
        test_T5_duplicate_gov_id_is_detected,
        test_T6_duplicate_exc_id_across_different_parent_rules_is_detected,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            print(f"FAIL: {test.__name__}: {exc}")
            failures += 1
        except Exception as exc:  # schema validation errors, etc.
            print(f"FAIL: {test.__name__}: {type(exc).__name__}: {exc}")
            failures += 1
        else:
            print(f"PASS: {test.__name__}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("path", nargs="?", help="Path to a governance.yaml file to check")
    group.add_argument("--self-test", action="store_true", help="Run the embedded self-tests instead")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if not args.path:
        parser.error("a path is required unless --self-test is given")
    return check_file(Path(args.path))


if __name__ == "__main__":
    sys.exit(main())
