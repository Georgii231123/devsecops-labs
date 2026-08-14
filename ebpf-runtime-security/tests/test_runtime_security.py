import json
from pathlib import Path

from scripts.event_triage import triage
from scripts.validate_policies import validate

ROOT = Path(__file__).resolve().parents[1]


def test_all_policies_pass_contract():
    for policy in (ROOT / "policies").glob("*.yaml"):
        assert validate(policy) == [], policy


def test_sensitive_file_event_is_high():
    event = json.loads((ROOT / "fixtures/events/sensitive-file.json").read_text())
    result = triage(event)
    assert result["severity"] == "high"
    assert result["rule"] == "sensitive-file-access"
    assert "/etc/shadow" in result["paths"]


def test_benign_file_event_is_informational():
    event = json.loads((ROOT / "fixtures/events/benign-file.json").read_text())
    result = triage(event)
    assert result["severity"] == "info"
    assert result["rule"] == "runtime-observation"
