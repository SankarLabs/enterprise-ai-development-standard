# EADS validation scripts

Python standard library only; Python 3.10+.

From a project repository root:

```bash
python scripts/validate_eads.py --check-structure
python scripts/validate_eads.py --check-gate implementation
python scripts/validate_eads.py --check-gate release
```

The project starter contains an unapproved state, so implementation and release checks should fail initially.

The gate validator checks required fields and rejects obvious agent/bot approver names. It does not authenticate a human, verify that evidence is genuine, or prevent local file edits. Enforce approval permissions through protected branches, CODEOWNERS, required reviewers and CI.
