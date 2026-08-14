from __future__ import annotations

from dataclasses import asdict, dataclass


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


@dataclass(slots=True)
class ProcessState:
    tank_level_pct: float = 45.0
    pressure_bar: float = 2.4
    pump_speed_pct: float = 35.0
    relief_valve_open: bool = False
    safe_state: bool = False

    def step(self, seconds: float = 1.0) -> None:
        if seconds <= 0:
            raise ValueError("seconds must be positive")

        inflow = (self.pump_speed_pct / 100.0) * 1.6
        outflow = 1.3 if self.relief_valve_open else 0.30
        self.tank_level_pct = _clamp(
            self.tank_level_pct + (inflow - outflow) * seconds,
            0.0,
            100.0,
        )

        target_pressure = (
            1.0
            + self.pump_speed_pct * 0.045
            + self.tank_level_pct * 0.012
            - (1.0 if self.relief_valve_open else 0.0)
        )
        response = min(seconds * 0.50, 1.0)
        self.pressure_bar = _clamp(
            self.pressure_bar + (target_pressure - self.pressure_bar) * response,
            0.0,
            10.0,
        )

    def snapshot(self) -> dict[str, float | bool]:
        return asdict(self)
