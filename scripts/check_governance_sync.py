#!/usr/bin/env python3
"""Keep generated project-starter/docs/*.md copies in sync with their
canonical methodology/*.md sources, and detect drift between them.

This is EADS standard-repository tooling only. It is not copied into
project-starter and is not expected to run inside a project repository
created by copying project-starter — that repository has no
methodology/ directory to compare against, and its distributed copies
become their own frozen reference once copied.

The canonical methodology/*.md files remain the sole authored governance
sources. This script never edits them; it only reads them and
writes/checks the generated distributed copies.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DOCUMENTS = [
    (Path("methodology/AGENT_GOVERNANCE.md"), Path("project-starter/docs/AGENT_GOVERNANCE.md")),
    (Path("methodology/APPROVAL_GATES.md"), Path("project-starter/docs/APPROVAL_GATES.md")),
]


def banner_for(canonical: Path) -> str:
    return (
        "> **Generated file — do not edit directly.**\n"
        f"> This is a distributed copy of the canonical source `{canonical}`\n"
        "> in the EADS standard repository (enterprise-ai-development-standard). Regenerate with\n"
        "> `python scripts/check_governance_sync.py --sync` after the canonical source changes.\n"
        "> Direct edits to this file will be overwritten and have no effect on the canonical standard.\n"
        "\n"
    )


def render(canonical_text: str, canonical: Path) -> str:
    return banner_for(canonical) + canonical_text


def strip_banner(distributed_text: str, canonical: Path) -> str | None:
    banner = banner_for(canonical)
    if not distributed_text.startswith(banner):
        return None
    return distributed_text[len(banner):]


def sync_one(root: Path, canonical: Path, distributed: Path) -> int:
    canonical_path = root / canonical
    distributed_path = root / distributed
    if not canonical_path.is_file():
        print(f"Missing canonical source: {canonical_path}")
        return 1
    canonical_text = canonical_path.read_text(encoding="utf-8")
    distributed_path.write_text(render(canonical_text, canonical), encoding="utf-8")
    print(f"Synced {distributed_path} from {canonical_path}.")
    return 0


def check_one(root: Path, canonical: Path, distributed: Path) -> int:
    canonical_path = root / canonical
    distributed_path = root / distributed
    if not canonical_path.is_file():
        print(f"Missing canonical source: {canonical_path}")
        return 1
    canonical_text = canonical_path.read_text(encoding="utf-8")

    if not distributed_path.is_file():
        print(f"Missing distributed copy: {distributed_path}")
        print("Run with --sync to generate it.")
        return 1
    distributed_text = distributed_path.read_text(encoding="utf-8")

    body = strip_banner(distributed_text, canonical)
    if body is None:
        print(f"{distributed_path} is missing the expected generated-file banner.")
        print("It may have been edited directly. Run with --sync to regenerate it from the canonical source.")
        return 1

    if body != canonical_text:
        print("GOVERNANCE DRIFT DETECTED:")
        print(f"- {distributed_path} no longer matches {canonical_path}.")
        print("Run with --sync to regenerate the distributed copy from the canonical source.")
        return 1

    print(f"OK: {distributed_path} matches the canonical source {canonical_path}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="EADS standard repository root")
    parser.add_argument("--sync", action="store_true", help="Regenerate the distributed copies from their canonical sources")
    args = parser.parse_args()
    root = args.root.resolve()

    worst = 0
    for canonical, distributed in DOCUMENTS:
        result = sync_one(root, canonical, distributed) if args.sync else check_one(root, canonical, distributed)
        worst = max(worst, result)
    return worst


if __name__ == "__main__":
    sys.exit(main())
