from __future__ import annotations

from pathlib import Path

import yaml

VALID_CRITICALITY = {"low", "medium", "high", "critical"}


class AssetInventory:
    def __init__(self, assets: list[dict[str, object]]) -> None:
        self.assets = assets

    @classmethod
    def from_file(cls, path: str | Path) -> "AssetInventory":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(data.get("assets", []))

    def validate(self, known_zones: set[str]) -> list[str]:
        errors: list[str] = []
        ids: set[str] = set()
        for asset in self.assets:
            asset_id = str(asset.get("id", ""))
            if not asset_id:
                errors.append("asset is missing id")
                continue
            if asset_id in ids:
                errors.append(f"duplicate asset id: {asset_id}")
            ids.add(asset_id)

            if asset.get("zone") not in known_zones:
                errors.append(f"{asset_id}: unknown zone {asset.get('zone')}")
            if asset.get("criticality") not in VALID_CRITICALITY:
                errors.append(f"{asset_id}: invalid criticality")
            protocols = asset.get("protocols")
            if not isinstance(protocols, list) or not protocols:
                errors.append(f"{asset_id}: protocols must be a non-empty list")
        return errors

    def by_id(self, asset_id: str) -> dict[str, object]:
        for asset in self.assets:
            if asset.get("id") == asset_id:
                return asset
        raise KeyError(asset_id)
