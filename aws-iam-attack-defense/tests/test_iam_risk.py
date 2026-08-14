import json
from pathlib import Path

from iam_risk import analyze, report

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "scenarios" / name).read_text())


def ids(name):
    return {finding.id for finding in analyze(load(name))}


def test_passrole_compute_is_detected():
    assert "IAM002" in ids("passrole-compute.json")


def test_policy_version_path_is_detected():
    assert "IAM003" in ids("policy-version.json")


def test_access_key_path_is_detected():
    assert "IAM005" in ids("access-key.json")


def test_wildcard_admin_is_critical():
    item = report("wildcard", load("wildcard-admin.json"))
    assert item["risk_score"] == 100


def test_secure_deployer_is_clean():
    assert analyze(load("secure-deployer.json")) == []
