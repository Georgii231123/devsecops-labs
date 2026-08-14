from pathlib import Path

from otlab.network import NetworkPolicy

ROOT = Path(__file__).resolve().parents[1]


def test_segmentation_contracts() -> None:
    policy = NetworkPolicy.from_file(ROOT / "config" / "network-policy.yaml")
    assert policy.decide("IT", "OT-Control", "modbus-tcp", "write") == "deny"
    assert policy.decide("OT-Supervisory", "OT-Control", "modbus-tcp", "read") == "allow"
    assert policy.decide("OT-Engineering", "OT-Control", "modbus-tcp", "write") == "allow"
    assert policy.decide("OT-Control", "Internet", "*", "*") == "deny"
