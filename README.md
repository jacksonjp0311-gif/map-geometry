# map-geometry

**An evolving runner built on Athar's claim-map swarm.**

Forked from [atharhive/colony](https://github.com/atharhive/colony) and turned into a cyclic system that can improve its own surfaces under measurement.

The original geometry stays load-bearing:
- Seven claims, each mapped to one intent
- Queen reads only the cluster map (settled / contested / single / blind / dead)
- Coverage first, escalation only where it pays
- No averaging. Disagreement is shown.
- HOLD when a load-bearing claim cannot be bought
- Independent bundle + sha256 verifier that never imports producer code

What this fork adds:
- Scheduled evolve cycles (`.github/workflows/map-evolve.yml`)
- Closed set of safe knobs (`colony/knobs.py`)
- Twin control: treatment may mutate, control is frozen
- Keep only when the trial window is strictly better *and* the twin does not lead
- Hard ceiling: tribute to the human principal, human authorize for durable accepts, append-only witness
- Oracle that can kill weak keeps

Not AGI. Not novel theorem discovery. The verifier stays outside the mutation set.

## Quick start

```bash
git clone https://github.com/jacksonjp0311-gif/map-geometry
cd map-geometry
python -m colony.evolve --cycles 2
python -m colony.evolve --status
```

## Relation to other work

- Original commercial swarm: https://github.com/atharhive/colony
- Governed agent society this runner draws from: https://github.com/jacksonjp0311-gif/agent-colony

See [CHARTER.md](CHARTER.md) for the hard ceiling.

MIT. Original by Athar. Evolving runner by James Paul Jackson.
