---
name: multi-model-council
description: Structure a council deliberation when the user explicitly asks for one, or when a consequential decision would benefit from independent model perspectives.
license: MIT
metadata:
  openclaw:
    emoji: "crown"
---

# Multi-Model Council

Produce a decision that makes evidence, disagreement, uncertainty, and the next
action clear.

## When to use

Use this skill for an explicit council, debate, deliberation, or war-table
request. It may also help with a consequential choice when genuinely independent
model perspectives are available and the added cost is justified. Handle
ordinary analysis directly.

A council does not replace current evidence, domain research, qualified advice,
or required authorization.

## Deliberation

1. Frame the decision, stakes, constraints, and what evidence could change it.
2. Select the smallest useful set of perspectives. Choose roles for the actual
   decision; do not default to a fixed roster.
3. Obtain independent views before sharing other participants' conclusions.
4. Add a clash or rebuttal round only when a material disagreement remains.
5. Synthesize the decision, preserving meaningful dissent and uncertainty.
6. End with a reversible next action or the exact blocker.

Use distinct models or agents when the runtime makes them available. Record
which perspectives were actually independent. If one model is simulating
several roles, say so; do not present simulated roles as multi-model evidence.

Do not manufacture dissent. Agreement can be a valid result. Confidence should
reflect evidence quality and unresolved assumptions, not a forced vote or a
simple average of self-reported scores.

## Output

Return a compact decision brief containing:

- decision or recommendation;
- strongest supporting evidence;
- material disagreement and what would resolve it;
- calibrated confidence and key assumptions;
- next action, owner, and stopping condition;
- authority or approval still required before any external effect.

Use only the context needed for the decision. Do not expose secrets or raw
private payloads to additional models or agents.
