# OpenClaw Skills by Ascendant Industries

Focused skills for [OpenClaw](https://github.com/openclaw/openclaw) agents.

## Skills

### multi-model-council

Structure a decision-focused deliberation when the user explicitly asks for a
council or when a consequential choice benefits from genuinely independent
model perspectives.

The skill scales the number of perspectives and rounds to the decision. It
distinguishes real multi-model evidence from perspectives simulated by one
model, preserves meaningful dissent without forcing it, and ends with a
bounded next action.

**Install:**

```bash
cp -r multi-model-council ~/.openclaw/workspace/skills/
```

**Invoke:**

```text
/council Should we open-source our agent framework?
```

## Assurance

Every skill must have a matching profile under `assurance/`, realistic routing
fixtures under `evals/`, and an exact SHA-256 identity.

Run the dependency-free structural gate:

```bash
python3 scripts/validate_skills.py
```

The promotion gate must remain blocked while a material change is
`REOPENED`:

```bash
python3 scripts/validate_skills.py --require-certified
```

Promotion requires repeated routing tests, behavioral comparison against the
same tasks without the skill, retained execution traces, pinned security scans,
and independent verification. A valid Markdown file is not a certified
capability.

The assurance baselines track the
[Agent Skills specification](https://github.com/agentskills/agentskills),
[OpenClaw skill runtime](https://github.com/openclaw/openclaw), and current
[Codex plugin examples](https://github.com/openai/plugins). External scanners
inform admission but never grant authority.

## About

These skills are maintained by
[Ascendant Industries](https://github.com/jeffgreen726-creator). Ascendant
treats models as replaceable workers: authority remains explicit, execution is
verifiable, and outcomes are measurable.

## License

MIT
