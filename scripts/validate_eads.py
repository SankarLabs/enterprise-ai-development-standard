#!/usr/bin/env python3
"""Validate EADS project structure and recorded approval gates.

This is a workflow guardrail, not an identity provider or tamper-proof control.
Use protected branches, required reviewers and CI for enterprise enforcement.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_DOCS = [
    "PROJECT_BRIEF.md", "SPEC.md", "ARCHITECTURE.md", "TECH_STACK.md",
    "CODE_STANDARDS.md", "TESTING_STRATEGY.md", "PLAN.md", "STATUS.md",
    "OPEN_QUESTIONS.md", "APPROVALS.md", "PROJECT_STATE.json",
]
IMPLEMENTATION_GATES = ["G0", "G1", "G2", "G3", "G4"]
RELEASE_GATES = IMPLEMENTATION_GATES + ["G5"]
FORBIDDEN_APPROVER_PATTERN = re.compile(r"\b(agent|assistant|llm|bot|claude|cursor|copilot|ai|model)\b", re.IGNORECASE)


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing approval state file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("gates"), dict):
        raise ValueError("PROJECT_STATE.json must contain a gates object.")
    return data


def check_structure(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_DOCS:
        path = root / "docs" / rel
        if not path.is_file():
            errors.append(f"Missing required document: docs/{rel}")
        elif path.stat().st_size == 0:
            errors.append(f"Empty required document: docs/{rel}")
    state_path = root / "docs" / "PROJECT_STATE.json"
    if state_path.exists():
        try:
            state = load_state(state_path)
            for gate in ["G0", "G1", "G2", "G3", "G4", "G5"]:
                if gate not in state["gates"]:
                    errors.append(f"Missing gate record: {gate}")
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def check_gate(root: Path, gate_name: str) -> list[str]:
    state = load_state(root / "docs" / "PROJECT_STATE.json")
    required = IMPLEMENTATION_GATES if gate_name == "implementation" else RELEASE_GATES
    errors: list[str] = []
    gates = state["gates"]
    for gate_id in required:
        record = gates.get(gate_id)
        if not isinstance(record, dict):
            errors.append(f"{gate_id}: missing gate record.")
            continue
        if record.get("status") != "approved":
            errors.append(f"{gate_id}: status must be 'approved' (found {record.get('status')!r}).")
            continue
        approver = str(record.get("approved_by", "")).strip()
        if not approver:
            errors.append(f"{gate_id}: approved_by is required.")
        elif FORBIDDEN_APPROVER_PATTERN.search(approver):
            errors.append(f"{gate_id}: approver identity appears to be an agent or bot: {approver!r}.")
        if not str(record.get("approved_at", "")).strip():
            errors.append(f"{gate_id}: approved_at is required.")
        if not str(record.get("scope", "")).strip():
            errors.append(f"{gate_id}: approval scope is required.")
        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(str(x).strip() for x in evidence):
            errors.append(f"{gate_id}: at least one evidence reference is required.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root (default: current directory)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check-structure", action="store_true")
    group.add_argument("--check-gate", choices=("implementation", "release"))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        errors = check_structure(root) if args.check_structure else check_gate(root, args.check_gate)
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("EADS validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EADS validation PASSED.")
    if args.check_gate:
        print("Note: this validates recorded fields only; it does not authenticate approvers or enforce repository permissions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
