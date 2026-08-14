from otlab.incidents import run_scenario


def test_unauthorized_write_drill_proves_rejection() -> None:
    report = run_scenario("unauthorized-modbus-write")
    assert len(report["alerts"]) >= 2
    assert report["process_state"]["pump_speed_pct"] == 35
    assert any("rejected" in action.lower() for action in report["actions"])


def test_high_pressure_drill_reaches_safe_state() -> None:
    report = run_scenario("high-pressure")
    assert report["process_state"]["safe_state"] is True
    assert report["process_state"]["pump_speed_pct"] == 10
    assert any(alert["rule_id"] == "OT-PROCESS-001" for alert in report["alerts"])
