from pathlib import Path

from otlab.detection import DetectionEngine

ROOT = Path(__file__).resolve().parents[1]


def test_it_modbus_write_generates_two_high_alerts() -> None:
    engine = DetectionEngine.from_file(ROOT / "config" / "detection-rules.yaml")
    event = {
        "source_asset": "it-workstation-01",
        "source_zone": "IT",
        "destination_zone": "OT-Control",
        "protocol": "modbus-tcp",
        "action": "write",
        "details": {"register": 10, "value": 100},
    }
    alerts = engine.analyze(event)
    assert {alert.rule_id for alert in alerts} == {"OT-MODBUS-001", "OT-ZONE-001"}


def test_high_pressure_generates_critical_alert() -> None:
    engine = DetectionEngine.from_file(ROOT / "config" / "detection-rules.yaml")
    alerts = engine.analyze(
        {
            "source_asset": "plc-01",
            "source_zone": "OT-Control",
            "destination_zone": "Monitoring",
            "protocol": "process",
            "action": "telemetry",
            "details": {"pressure_bar": 5.7},
        }
    )
    assert any(alert.rule_id == "OT-PROCESS-001" for alert in alerts)
