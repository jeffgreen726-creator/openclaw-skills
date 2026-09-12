#!/usr/bin/env python3
"""Validate skill structure, routing fixtures, and Ascendant assurance state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
CERTIFICATION_STATES = {"REOPENED", "RECERTIFIED", "RETIRED"}
GATE_STATES = {"NOT_RUN", "PASS", "FAIL", "BLOCKED"}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path.relative_to(ROOT)}: missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"{path.relative_to(ROOT)}: missing closing frontmatter delimiter")

    frontmatter: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in ALLOWED_FRONTMATTER:
            fail(f"{path.relative_to(ROOT)}: unsupported frontmatter key {key!r}")
        frontmatter[key] = value.strip().strip("'\"")

    return frontmatter, text


def validate_skill(path: Path, assurance: dict) -> None:
    frontmatter, text = parse_frontmatter(path)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    license_name = frontmatter.get("license", "")

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(f"{path.relative_to(ROOT)}: invalid skill name {name!r}")
    if path.parent.name != name:
        fail(f"{path.relative_to(ROOT)}: name must match parent directory")
    if not description or len(description) > 1024:
        fail(f"{path.relative_to(ROOT)}: description must contain 1-1024 characters")
    if len(description) > 240:
        fail(f"{path.relative_to(ROOT)}: local discovery budget is 240 characters")
    if len(text.splitlines()) > 500:
        fail(f"{path.relative_to(ROOT)}: SKILL.md exceeds 500-line context budget")
    if not license_name:
        fail(f"{path.relative_to(ROOT)}: license must be declared")
    if not (ROOT / "LICENSE").is_file():
        fail("repository LICENSE file is missing")

    artifact = assurance.get("artifact", {})
    relative = path.relative_to(ROOT).as_posix()
    if artifact.get("path") != relative:
        fail(f"{relative}: assurance artifact path mismatch")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if artifact.get("sha256") != digest:
        fail(f"{relative}: assurance hash mismatch; reopen and update evidence identity")
    if artifact.get("license") != license_name:
        fail(f"{relative}: assurance license mismatch")


def validate_routing(assurance: dict) -> None:
    gate = assurance.get("routing_gate", {})
    path = ROOT / str(gate.get("cases_path", ""))
    data = load_json(path)
    if data.get("skill_name") != assurance.get("skill_name"):
        fail(f"{path.relative_to(ROOT)}: skill name mismatch")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 20:
        fail(f"{path.relative_to(ROOT)}: at least 20 routing cases required")

    ids: set[str] = set()
    prompts: set[str] = set()
    positives = negatives = near_miss_negatives = 0
    for case in cases:
        if not isinstance(case, dict):
            fail(f"{path.relative_to(ROOT)}: every case must be an object")
        case_id = case.get("id")
        prompt = case.get("prompt")
        should_trigger = case.get("should_trigger")
        near_miss = case.get("near_miss")
        if not isinstance(case_id, str) or not case_id:
            fail(f"{path.relative_to(ROOT)}: case id missing")
        if case_id in ids:
            fail(f"{path.relative_to(ROOT)}: duplicate case id {case_id}")
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            fail(f"{path.relative_to(ROOT)}: prompt too short for {case_id}")
        if prompt in prompts:
            fail(f"{path.relative_to(ROOT)}: duplicate prompt for {case_id}")
        if not isinstance(should_trigger, bool) or not isinstance(near_miss, bool):
            fail(f"{path.relative_to(ROOT)}: labels must be booleans for {case_id}")
        ids.add(case_id)
        prompts.add(prompt)
        if should_trigger:
            positives += 1
        else:
            negatives += 1
            near_miss_negatives += int(near_miss)

    if positives < 8 or negatives < 8 or near_miss_negatives < 8:
        fail(f"{path.relative_to(ROOT)}: require >=8 positive, negative, and near-miss negative cases")
    if gate.get("runs_per_case", 0) < 3:
        fail("routing gate requires at least three runs per case")
    for field in ("minimum_precision", "minimum_recall"):
        value = gate.get(field)
        if not isinstance(value, (int, float)) or value < 0.9 or value > 1:
            fail(f"routing gate {field} must be between 0.9 and 1.0")


def validate_assurance(path: Path) -> dict:
    data = load_json(path)
    if data.get("schema_version") != 1:
        fail(f"{path.relative_to(ROOT)}: unsupported schema version")
    name = data.get("skill_name")
    if not isinstance(name, str) or not name:
        fail(f"{path.relative_to(ROOT)}: skill_name missing")
    if data.get("certification_state") not in CERTIFICATION_STATES:
        fail(f"{path.relative_to(ROOT)}: invalid certification state")

    for section in ("routing_gate", "behavioral_gate", "security_gate", "promotion_gate"):
        status = data.get(section, {}).get("status")
        if status not in GATE_STATES:
            fail(f"{path.relative_to(ROOT)}: invalid {section} status {status!r}")

    baselines = data.get("compatibility", [])
    if len(baselines) < 2:
        fail(f"{path.relative_to(ROOT)}: compatibility baselines missing")
    for baseline in baselines:
        if not re.fullmatch(r"[0-9a-f]{40}", str(baseline.get("baseline_commit", ""))):
            fail(f"{path.relative_to(ROOT)}: baseline commit must be a full SHA")

    required = data.get("security_gate", {}).get("required", [])
    if len(required) < 2:
        fail(f"{path.relative_to(ROOT)}: two independent security tools required")
    if len(data.get("behavioral_gate", {}).get("required_invariants", [])) < 6:
        fail(f"{path.relative_to(ROOT)}: behavioral invariant coverage is incomplete")
    if len(data.get("recertification_triggers", [])) < 4:
        fail(f"{path.relative_to(ROOT)}: recertification triggers are incomplete")

    validate_routing(data)
    validate_skill(ROOT / data["artifact"]["path"], data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-certified",
        action="store_true",
        help="Fail unless every assurance profile is RECERTIFIED with passing gates and evidence.",
    )
    args = parser.parse_args()

    profiles = sorted((ROOT / "assurance").glob("*.json"))
    skills = sorted(ROOT.glob("*/SKILL.md"))
    if not profiles or not skills:
        fail("at least one skill and assurance profile are required")

    validated: dict[str, dict] = {}
    for profile in profiles:
        data = validate_assurance(profile)
        validated[data["skill_name"]] = data

    skill_names = {path.parent.name for path in skills}
    if skill_names != set(validated):
        fail("every skill must have exactly one assurance profile")

    print(f"PASS: structural assurance for {len(skill_names)} skill(s)")
    for name in sorted(validated):
        data = validated[name]
        print(
            f"{name}: certification={data['certification_state']} "
            f"promotion={data['promotion_gate']['status']}"
        )

    if args.require_certified:
        for name, data in validated.items():
            gates = (
                data["routing_gate"]["status"],
                data["behavioral_gate"]["status"],
                data["security_gate"]["status"],
                data["promotion_gate"]["status"],
            )
            if (
                data["certification_state"] != "RECERTIFIED"
                or gates != ("PASS", "PASS", "PASS", "PASS")
                or not data.get("evidence_receipts")
            ):
                print(f"BLOCKED: {name} is not independently recertified", file=sys.stderr)
                return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
