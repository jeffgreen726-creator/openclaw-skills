# OpenClaw Skills by Ascendant Industries

Custom skills for [OpenClaw](https://github.com/openclaw/openclaw) agents. Built by a team that runs autonomous multi-model AI councils in production.

## Skills

### multi-model-council

Turn any question into a structured debate between competing AI perspectives. Instead of one model's best guess, get a deliberated verdict from 8 specialized seats.

**Use cases:**
- Product strategy decisions
- Architecture and tech stack choices
- Risk assessment and threat modeling
- Investment thesis evaluation
- Any decision where a single perspective isn't enough

**Install:**
```bash
# Copy the skill into your OpenClaw workspace
cp -r multi-model-council ~/.openclaw/workspace/skills/
```

**Invoke:**
```
/council Should we open-source our agent framework?
```

## About

These skills are extracted from [Kingmaker](https://github.com/jeffgreen726-creator/kingmaker) — a multi-agent intelligence system that runs 17-seat AI councils, 6 temporal agents with evolutionary learning, and autonomous paper trading on Polymarket.

The thesis: every AI company ships one model's best guess. We built a system where multiple models argue, dissent, and reach verdicts through structured deliberation — then act on those verdicts autonomously.

## License

MIT
