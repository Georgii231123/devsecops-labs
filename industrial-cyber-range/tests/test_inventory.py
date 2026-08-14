from pathlib import Path

import yaml

from otlab.inventory import AssetInventory

ROOT = Path(__file__).resolve().parents[1]


def test_asset_inventory_is_consistent() -> None:
    zones = yaml.safe_load((ROOT / "config" / "zones.yaml").read_text(encoding="utf-8"))
    inventory = AssetInventory.from_file(ROOT / "config" / "assets.yaml")
    assert inventory.validate(set(zones["zones"])) == []
    assert inventory.by_id("plc-01")["criticality"] == "critical"
