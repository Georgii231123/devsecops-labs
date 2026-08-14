#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import yaml

from otlab.inventory import AssetInventory
from otlab.network import NetworkPolicy

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    zones_data = yaml.safe_load((ROOT / "config" / "zones.yaml").read_text(encoding="utf-8"))
    zones = set(zones_data["zones"])
    inventory = AssetInventory.from_file(ROOT / "config" / "assets.yaml")
    errors = inventory.validate(zones)

    policy = NetworkPolicy.from_file(ROOT / "config" / "network-policy.yaml")
    contracts = [
        (
            policy.decide("IT", "OT-Control", "modbus-tcp", "write") == "deny",
            "IT must not write directly to OT-Control",
        ),
        (
            policy.decide("OT-Supervisory", "OT-Control", "modbus-tcp", "read") == "allow",
            "SCADA read path must be allowed",
        ),
        (
            policy.decide("OT-Engineering", "OT-Control", "modbus-tcp", "write") == "allow",
            "engineering control path must be allowed",
        ),
        (
            policy.decide("OT-Control", "Internet", "*", "*") == "deny",
            "PLC direct Internet path must be denied",
        ),
    ]
    errors.extend(message for ok, message in contracts if not ok)

    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    for service in ("plc", "opcua", "mqtt", "scada", "prometheus", "grafana"):
        ports = compose["services"][service].get("ports", [])
        for mapping in ports:
            if not str(mapping).startswith("127.0.0.1:"):
                errors.append(f"{service}: host port must bind to loopback: {mapping}")
    for network in ("ot_control", "ot_supervisory", "ot_dmz", "monitoring"):
        if not compose["networks"][network].get("internal"):
            errors.append(f"{network}: OT lab network must be internal")

    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    print("Industrial cyber range architecture: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
