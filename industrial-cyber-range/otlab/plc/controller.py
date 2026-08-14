from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from otlab.plant import ProcessState
from otlab.safety import apply_safe_state, should_enter_safe_state


class UnauthorizedWrite(PermissionError):
    pass


@dataclass(frozen=True, slots=True)
class AuditEvent:
    timestamp: str
    source: str
    action: str
    register: int | None
    value: int | None
    outcome: str
    detail: str


class PLCController:
    def __init__(
        self,
        state: ProcessState | None = None,
        allowed_writers: set[str] | None = None,
    ) -> None:
        self.state = state or ProcessState()
        self.allowed_writers = allowed_writers or {"engineering-01", "scada-01"}
        self.audit: list[AuditEvent] = []

    def _record(
        self,
        source: str,
        action: str,
        register: int | None,
        value: int | None,
        outcome: str,
        detail: str,
    ) -> None:
        self.audit.append(
            AuditEvent(
                timestamp=datetime.now(UTC).isoformat(),
                source=source,
                action=action,
                register=register,
                value=value,
                outcome=outcome,
                detail=detail,
            )
        )

    def read_register(self, address: int) -> int:
        mapping = {
            0: round(self.state.tank_level_pct * 10),
            1: round(self.state.pressure_bar * 100),
            10: round(self.state.pump_speed_pct),
            11: int(self.state.relief_valve_open),
            12: int(self.state.safe_state),
        }
        if address not in mapping:
            raise KeyError(f"unknown register: {address}")
        return mapping[address]

    def read_registers(self, start: int, quantity: int) -> list[int]:
        if quantity < 1 or quantity > 125:
            raise ValueError("quantity outside Modbus limits")
        return [self.read_register(address) for address in range(start, start + quantity)]

    def write_register(self, source: str, address: int, value: int) -> None:
        if source not in self.allowed_writers:
            self._record(source, "write", address, value, "rejected", "writer not authorized")
            raise UnauthorizedWrite(source)

        if address == 10:
            if not 0 <= value <= 100:
                raise ValueError("pump speed must be between 0 and 100")
            if self.state.safe_state and value > 10:
                raise ValueError("safe state limits pump speed to 10%")
            self.state.pump_speed_pct = float(value)
        elif address == 11:
            if value not in {0, 1}:
                raise ValueError("relief valve accepts only 0 or 1")
            if self.state.safe_state and value == 0:
                raise ValueError("safe state keeps relief valve open")
            self.state.relief_valve_open = bool(value)
        else:
            raise KeyError(f"register {address} is not writable")

        self._record(source, "write", address, value, "accepted", "write applied")

    def tick(self, seconds: float = 1.0) -> None:
        self.state.step(seconds)
        reason = should_enter_safe_state(self.state)
        if reason and not self.state.safe_state:
            apply_safe_state(self.state, reason)
            self._record("safety-controller", "safe-state", None, None, "applied", reason)
