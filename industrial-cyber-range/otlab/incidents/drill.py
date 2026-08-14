from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import yaml

from otlab.detection import DetectionEngine
from otlab.plc import PLCController, UnauthorizedWrite

ROOT = Path(__file__).resolve().parents[2]


def _event_for_unauthorized_write() -> dict[str, object]:
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "source_asset": "it-workstation-01",
        "source_zone": "IT",
        "destination_asset": "plc-01",
        "destination_zone": "OT-Control",
        "protocol": "modbus-tcp",
        "action": "write",
        "details": {"register": 10, "value": 100},
    }


def run_scenario(name: str) -> dict[str, object]:
    scenario_path = ROOT / "incidents" / "scenarios" / f"{name}.yaml"
    scenario = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
    engine = DetectionEngine.from_file(ROOT / "config" / "detection-rules.yaml")
    controller = PLCController()
    started = datetime.now(UTC).isoformat()
    alerts = []
    actions: list[str] = []

    if name == "unauthorized-modbus-write":
        event = _event_for_unauthorized_write()
        alerts.extend(alert.to_dict() for alert in engine.analyze(event))
        try:
            controller.write_register("it-workstation-01", 10, 100)
        except UnauthorizedWrite:
            actions.append("PLC rejected write from unauthorized asset")

    elif name == "high-pressure":
        controller.write_register("engineering-01", 10, 100)
        actions.append("engineering command raised simulated pump speed")
        for _ in range(10):
            controller.tick(1.0)
            if controller.state.safe_state:
                break
        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "source_asset": "plc-01",
            "source_zone": "OT-Control",
            "destination_asset": "monitoring-01",
            "destination_zone": "Monitoring",
            "protocol": "process",
            "action": "telemetry",
            "details": {"pressure_bar": controller.state.pressure_bar},
        }
        alerts.extend(alert.to_dict() for alert in engine.analyze(event))
        actions.append("safety controller evaluated process thresholds")
    else:
        raise ValueError(f"unsupported scenario: {name}")

    return {
        "scenario": scenario.get("name", name),
        "started_at": started,
        "completed_at": datetime.now(UTC).isoformat(),
        "expected_control": scenario.get("expected_control"),
        "alerts": alerts,
        "actions": actions,
        "process_state": controller.state.snapshot(),
        "audit_events": [asdict(event) for event in controller.audit],
    }
