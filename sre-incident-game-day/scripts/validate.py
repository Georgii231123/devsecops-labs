#!/usr/bin/env python3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

config = yaml.safe_load((ROOT / "prometheus" / "prometheus.yml").read_text())
rules = yaml.safe_load((ROOT / "prometheus" / "alerts.yml").read_text())
runbook = (ROOT / "runbooks" / "high-error-rate.md").read_text()

assert config["global"]["scrape_interval"] == "1s"
assert config["global"]["evaluation_interval"] == "1s"
assert config["scrape_configs"][0]["static_configs"][0]["targets"] == ["service:8000"]

alerts = {rule["alert"]: rule for group in rules["groups"] for rule in group["rules"]}
assert alerts["ApplicationFailureMode"]["labels"]["severity"] == "page"
assert alerts["ApplicationFailureMode"]["for"] == "3s"
assert "app_failure_mode == 1" in alerts["ApplicationFailureMode"]["expr"]
assert "High5xxVolume" in alerts

for section in ["Detection", "Triage", "Containment", "Remediation", "Verification", "Rollback", "Post-incident"]:
    assert f"## {section}" in runbook, f"missing runbook section: {section}"

print("SRE game-day configuration checks passed")
