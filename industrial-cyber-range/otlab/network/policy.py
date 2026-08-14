from __future__ import annotations

from pathlib import Path

import yaml


class NetworkPolicy:
    def __init__(self, rules: list[dict[str, object]], default: str = "deny") -> None:
        self.rules = rules
        self.default = default

    @classmethod
    def from_file(cls, path: str | Path) -> NetworkPolicy:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(data.get("rules", []), data.get("default", "deny"))

    def decide(
        self,
        source: str,
        destination: str,
        protocol: str,
        action: str,
    ) -> str:
        for rule in self.rules:
            if rule.get("source") not in {source, "*"}:
                continue
            if rule.get("destination") not in {destination, "*"}:
                continue
            if rule.get("protocol") not in {protocol, "*"}:
                continue
            actions = rule.get("actions", [])
            if isinstance(actions, list) and action not in actions and "*" not in actions:
                continue
            return str(rule.get("effect", self.default))
        return self.default
