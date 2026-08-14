from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True, slots=True)
class Alert:
    rule_id: str
    severity: str
    summary: str
    event: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class DetectionEngine:
    def __init__(self, config: dict[str, object]) -> None:
        self.config = config

    @classmethod
    def from_file(cls, path: str | Path) -> DetectionEngine:
        return cls(yaml.safe_load(Path(path).read_text(encoding="utf-8")))

    def analyze(self, event: dict[str, object]) -> list[Alert]:
        alerts: list[Alert] = []
        protocol = str(event.get("protocol", ""))
        action = str(event.get("action", ""))
        source_asset = str(event.get("source_asset", ""))
        source_zone = str(event.get("source_zone", ""))
        destination_zone = str(event.get("destination_zone", ""))
        details = event.get("details", {})
        details = details if isinstance(details, dict) else {}

        writers = set(self.config.get("authorized_modbus_writers", []))
        if protocol == "modbus-tcp" and action == "write" and source_asset not in writers:
            alerts.append(
                Alert(
                    "OT-MODBUS-001",
                    "high",
                    f"unauthorized Modbus write from {source_asset}",
                    event,
                )
            )

        if source_zone == "IT" and destination_zone == "OT-Control":
            alerts.append(
                Alert(
                    "OT-ZONE-001",
                    "high",
                    "IT source attempted direct access to OT-Control",
                    event,
                )
            )

        allowed_clients = set(self.config.get("allowed_opcua_clients", []))
        if protocol == "opcua" and source_asset and source_asset not in allowed_clients:
            alerts.append(
                Alert(
                    "OT-OPCUA-001",
                    "medium",
                    f"unknown OPC UA client {source_asset}",
                    event,
                )
            )

        prefixes = tuple(str(item) for item in self.config.get("allowed_mqtt_prefixes", []))
        topic = str(details.get("topic", ""))
        if protocol == "mqtt" and topic and prefixes and not topic.startswith(prefixes):
            alerts.append(
                Alert("OT-MQTT-001", "medium", f"unexpected MQTT topic {topic}", event)
            )

        thresholds = self.config.get("thresholds", {})
        thresholds = thresholds if isinstance(thresholds, dict) else {}
        pressure = details.get("pressure_bar")
        high_pressure = float(thresholds.get("pressure_high_bar", 5.5))
        if isinstance(pressure, (int, float)) and float(pressure) >= high_pressure:
            alerts.append(
                Alert(
                    "OT-PROCESS-001",
                    "critical",
                    f"process pressure is above {high_pressure} bar",
                    event,
                )
            )

        return alerts
