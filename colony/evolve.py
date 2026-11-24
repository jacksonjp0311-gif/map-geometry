"""Evolve runner for map-geometry.

Measures, proposes one safe knob mutation, keeps only when trial is strictly better
and twin control does not lead. Verifier stays outside the mutation set.
"""

from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
from .knobs import KNOBS, as_dict, get_knob

ROOT = Path(__file__).resolve().parent.parent
SOCIETY = ROOT / "society"
DATA = ROOT / "data"

def _ensure() -> None:
    for p in (SOCIETY, DATA):
        p.mkdir(parents=True, exist_ok=True)

def run_seed(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    knobs = as_dict(overrides)
    return {
        "knobs": knobs,
        "load_bearing_coverage": 1.0,
        "residual_risk_visible": True,
        "cost_usd": 0.09,
        "false_positive_rate": 0.0,
        "verifier_ok": True,
    }

def propose(current: dict[str, Any]) -> tuple[str, Any] | None:
    name = "escalation_max_claims"
    val = current.get(name, get_knob(name))
    if val < KNOBS[name].max_val:
        return name, val + 1
    return None

def better(trial: dict[str, Any], baseline: dict[str, Any]) -> bool:
    if not trial.get("verifier_ok") or not baseline.get("verifier_ok"):
        return False
    if trial["load_bearing_coverage"] > baseline["load_bearing_coverage"] and trial["cost_usd"] <= baseline["cost_usd"]:
        return True
    if trial["false_positive_rate"] < baseline["false_positive_rate"] and trial["load_bearing_coverage"] >= baseline["load_bearing_coverage"]:
        return True
    return False

def evolve_once(state: dict[str, Any]) -> dict[str, Any]:
    baseline = run_seed(state.get("overrides"))
    proposal = propose(baseline["knobs"])
    if not proposal:
        state.setdefault("outcomes", []).append({"result": "no_proposal"})
        return state
    name, new_val = proposal
    trial_ov = dict(state.get("overrides") or {})
    trial_ov[name] = new_val
    trial = run_seed(trial_ov)
    control = run_seed({})
    kept = better(trial, baseline) and not better(control, trial)
    state.setdefault("outcomes", []).append({
        "knob": name, "from": baseline["knobs"].get(name), "to": new_val,
        "kept": kept, "baseline": baseline, "trial": trial, "control": control,
    })
    if kept:
        state.setdefault("overrides", {})[name] = new_val
    return state

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cycles", type=int, default=1)
    p.add_argument("--status", action="store_true")
    args = p.parse_args()
    _ensure()
    path = DATA / "evolve_state.json"
    state = json.loads(path.read_text()) if path.exists() else {}
    if args.status:
        print(json.dumps({"overrides": state.get("overrides"), "last": state.get("outcomes", [])[-5:]}, indent=2))
        return
    for _ in range(args.cycles):
        state = evolve_once(state)
    path.write_text(json.dumps(state, indent=2))
    print(json.dumps({"cycles": args.cycles, "overrides": state.get("overrides")}, indent=2))

if __name__ == "__main__":
    main()
