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

## About

These skills are maintained by
[Ascendant Industries](https://github.com/jeffgreen726-creator). Ascendant
treats models as replaceable workers: authority remains explicit, execution is
verifiable, and outcomes are measurable.

## License

MIT
