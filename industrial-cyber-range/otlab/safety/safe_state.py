from __future__ import annotations

from dataclasses import dataclass

from otlab.plant import ProcessState

PRESSURE_LIMIT_BAR = 5.5
LEVEL_LIMIT_PCT = 92.0


@dataclass(frozen=True, slots=True)
class SafetyTransition:
    reason: str
    previous_pump_speed_pct: float
    previous_relief_valve_open: bool


def should_enter_safe_state(state: ProcessState) -> str | None:
    if state.pressure_bar >= PRESSURE_LIMIT_BAR:
        return f"pressure >= {PRESSURE_LIMIT_BAR} bar"
    if state.tank_level_pct >= LEVEL_LIMIT_PCT:
        return f"tank level >= {LEVEL_LIMIT_PCT}%"
    return None


def apply_safe_state(state: ProcessState, reason: str) -> SafetyTransition:
    transition = SafetyTransition(
        reason=reason,
        previous_pump_speed_pct=state.pump_speed_pct,
        previous_relief_valve_open=state.relief_valve_open,
    )
    state.safe_state = True
    state.pump_speed_pct = 10.0
    state.relief_valve_open = True
    return transition
