# EADS project validator

Run from the project root:

```bash
python scripts/validate_eads.py --check-structure
python scripts/validate_eads.py --check-gate implementation
python scripts/validate_eads.py --check-gate release
```

The approval validator checks recorded fields only. It does not authenticate approvers or prevent local file edits. Use protected branches, required reviewers, CODEOWNERS and CI for enterprise enforcement.
