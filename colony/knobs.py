"""Closed set of safe knobs the evolve runner may propose."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Knob:
    name: str
    default: Any
    min_val: Any | None = None
    max_val: Any | None = None
    description: str = ""

KNOBS: dict[str, Knob] = {
    "escalation_max_claims": Knob("escalation_max_claims", 2, 0, 4, "Max claims that may receive extra scouts."),
    "single_source_penalty": Knob("single_source_penalty", 1, 0, 2, "How hard single-sourced load-bearing claims are treated."),
    "coverage_priority_boost": Knob("coverage_priority_boost", 0, -10, 10, "Priority adjustment for load-bearing claims."),
}

def get_knob(name: str, overrides: dict[str, Any] | None = None) -> Any:
    if name not in KNOBS:
        raise KeyError(f"unknown knob: {name}")
    if overrides and name in overrides:
        return overrides[name]
    return KNOBS[name].default

def as_dict(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    return {k: get_knob(k, overrides) for k in KNOBS}
