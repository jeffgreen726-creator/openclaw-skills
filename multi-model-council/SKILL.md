---
name: multi-model-council
description: "Run structured multi-model AI deliberations. Use when you need a decision that benefits from multiple perspectives — product strategy, architecture choices, risk assessment, or any question where a single model's answer isn't enough. Invoke with /council or when the user asks for a 'debate', 'deliberation', 'council session', or 'war table'."
homepage: https://github.com/jeffgreen726-creator/openclaw-skills
metadata:
  openclaw:
    emoji: "crown"
    requires:
      bins: ["curl", "jq"]
---

# Multi-Model Council — Structured AI Deliberation

Turn any question into a structured debate between multiple AI perspectives. Instead of getting one model's best guess, get a deliberated verdict from competing viewpoints.

## How It Works

The council runs in rounds:

1. **Frame** — Define the question, stakes, and constraints
2. **Inner Ring** — 4 specialized perspectives deliberate independently
3. **Clash** — Identify disagreements and force direct confrontation
4. **Outer Ring** — 4 fresh perspectives weigh in on the clash points
5. **Vote** — All seats vote with confidence scores
6. **Verdict** — Synthesize into a final decision with dissent noted

## Quick Start

When the user asks for a council deliberation, run this process:

### Step 1: Define the Seats

Choose 4 inner + 4 outer perspectives relevant to the question. Default roster:

**Inner Ring (core deliberation):**
- **Strategist** — Long-term thinking, competitive positioning, market dynamics
- **Operator** — Execution feasibility, resource constraints, timelines
- **Contrarian** — Challenge assumptions, find blind spots, stress-test logic
- **Revenue** — Monetization, unit economics, customer willingness to pay

**Outer Ring (fresh eyes):**
- **Technical** — Architecture, scalability, tech debt implications
- **Creative** — Novel approaches, unconventional solutions, reframing
- **Risk** — Downside scenarios, regulatory, reputation, security
- **Market** — Customer signals, competitive landscape, timing

### Step 2: Run the Deliberation

For each seat, generate a response to the question from that seat's perspective. Use this prompt template per seat:

```
You are the [SEAT_NAME] on a strategic council. Your role: [SEAT_DESCRIPTION].

Question: [USER_QUESTION]
Context: [ANY_CONTEXT]

Provide your analysis in this format:
## Position
[Your stance in 1-2 sentences]

## Reasoning
[Key arguments, 3-5 bullet points]

## Confidence
[0-100, with brief justification]

## Risk Flag
[One thing the council might be missing]
```

### Step 3: Detect Clashes

After inner ring deliberation, identify where seats disagree:
- Positions that directly contradict each other
- Confidence scores that diverge significantly (>30 point spread)
- Risk flags that challenge another seat's core assumption

Present clashes to outer ring seats for additional perspective.

### Step 4: Synthesize Verdict

Combine all perspectives into a structured verdict:

```
## Verdict
[The decision, stated clearly]

## Confidence: [weighted average]

## Consensus Points
[What everyone agreed on]

## Key Dissent
[Who disagreed and why — this is valuable signal, not noise]

## Action Items
[Concrete next steps, ordered by priority]

## Risk Watch
[Top 2-3 things to monitor that could invalidate this verdict]
```

## Advanced: Custom Seat Rosters

For domain-specific questions, swap in specialized seats:

**Product Launch:**
- Growth, UX, Engineering, Legal (inner)
- Finance, Support, Sales, Marketing (outer)

**Technical Architecture:**
- Backend, Frontend, DevOps, Security (inner)
- Performance, UX, Data, Cost (outer)

**Investment/Trading:**
- Fundamental, Technical, Macro, Sentiment (inner)
- Risk, Regulatory, Timing, Contrarian (outer)

## Tips

- The **Contrarian seat is the most valuable**. If all seats agree, the deliberation isn't doing its job — push the contrarian harder.
- **Confidence calibration**: Seats that are always 90%+ confident are poorly calibrated. Good seats express genuine uncertainty.
- **Dissent is signal**. A unanimous verdict with no dissent is suspicious. Always surface and preserve minority opinions.
- For high-stakes decisions, run the council twice with different seat assignments and compare verdicts.

## Example

User: "Should we open-source our internal agent framework?"

The council would deliberate with:
- Strategist weighing competitive moat vs ecosystem effects
- Revenue analyzing monetization impact
- Contrarian challenging the "open source = growth" assumption
- Technical evaluating maintenance burden
- And 4 more outer ring perspectives...

Producing a verdict like: "Open-source the framework with a proprietary orchestration layer. Confidence: 72%. Key dissent: Revenue seat argues hosted-first strategy generates more ARR. Risk watch: maintenance burden on a team of 1."

## Credits

Built by [Ascendant Industries](https://github.com/jeffgreen726-creator) — AI that argues, builds, and sells.
