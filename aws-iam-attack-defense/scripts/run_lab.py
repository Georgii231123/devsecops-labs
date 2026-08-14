from __future__ import annotations

import json
from pathlib import Path

from iam_risk import report

root = Path(__file__).resolve().parents[1]
scenario_dir = root / "scenarios"
out_dir = root / "artifacts"
out_dir.mkdir(exist_ok=True)

expected_vulnerable = {"wildcard-admin", "passrole-compute", "policy-version", "access-key"}
results = []
for path in sorted(scenario_dir.glob("*.json")):
    policy = json.loads(path.read_text())
    item = report(path.stem, policy)
    results.append(item)
    if path.stem in expected_vulnerable:
        assert item["finding_count"] > 0, path.stem
        assert item["risk_score"] >= 70, item
    elif path.stem == "secure-deployer":
        assert item["finding_count"] == 0, item

(out_dir / "iam-risk-report.json").write_text(json.dumps(results, indent=2))
lines = ["# IAM risk report", ""]
for item in results:
    lines.append(f"## {item['policy']}: score {item['risk_score']}/100")
    if not item["findings"]:
        lines.append("- no modeled escalation path detected")
    for finding in item["findings"]:
        lines.append(f"- **{finding['severity']} {finding['id']}** — {finding['title']}")
    lines.append("")
(out_dir / "iam-risk-report.md").write_text("\n".join(lines))
print("IAM attack/defense scenarios validated")
