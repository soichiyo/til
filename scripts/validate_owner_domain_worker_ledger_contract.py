#!/usr/bin/env python3
"""Validate the public-safe Owner / Domain / Worker ledger contract."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path


REQUIRED_TEXT = (
    "# Public Owner / Domain / Worker Ledger Contract",
    "owner: personal/soichiyo",
    "scope: project/soichiyo/til",
    "visibility: public-safe-contract",
    "private_owner_ledger: pull-by-reference",
    "distribution: default-deny",
    "domains: []",
    "workers: []",
    "## Lifecycle contract",
    "**Creation:**",
    "**Return:**",
    "**Acceptance:**",
    "**Closure:**",
    "**Retention:**",
    "**Onboarding:**",
    "**Offboarding:**",
    "**Archive or disable rollback:**",
    "## Distribution rule",
)

FORBIDDEN_TEXT = (
    "distribution: enabled",
    "distribution: allow",
    "task_id:",
    "client:",
    "credential:",
    "token:",
    "private_key:",
)


def validate(text: str) -> list[str]:
    """Return deterministic validation errors for a contract document."""
    errors = [f"missing required text: {item}" for item in REQUIRED_TEXT if item not in text]
    errors.extend(f"forbidden public content: {item}" for item in FORBIDDEN_TEXT if item in text)
    return errors


def validate_path(path: Path) -> int:
    errors = validate(path.read_text(encoding="utf-8"))
    if errors:
        print(f"FAIL: {path}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {path}")
    return 0


def self_test(contract_path: Path) -> int:
    valid = contract_path.read_text(encoding="utf-8")
    cases = {
        "non-empty-domain-entry": valid.replace("domains: []", "domains:\n  - public-example"),
        "non-empty-worker-entry": valid.replace("workers: []", "workers:\n  - public-example"),
        "enabled-distribution": valid.replace("distribution: default-deny", "distribution: enabled"),
        "private-task-history": valid + "\ntask_id: internal-only\n",
    }
    failures = []
    for name, candidate in cases.items():
        if not validate(candidate):
            failures.append(name)
    if failures:
        print(f"FAIL: self-test accepted invalid case(s): {', '.join(failures)}")
        return 1
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory) / "contract.md"
        temporary_path.write_text(valid, encoding="utf-8")
        if validate_path(temporary_path) != 0:
            return 1
    print("PASS: self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs" / "owner-domain-worker-ledger-contract.md",
    )
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if validate_path(arguments.file) != 0:
        return 1
    return self_test(arguments.file) if arguments.self_test else 0


if __name__ == "__main__":
    raise SystemExit(main())
