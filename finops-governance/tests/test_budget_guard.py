from scripts.budget_guard import evaluate


def test_budget_evaluation_passes_with_headroom():
    policy = {
        "forecast_multiplier": 1.1,
        "team_budgets": {"platform": 100.0},
    }
    allocation = {"records": [{"team": "platform", "cost": 80.0}]}
    rows, failures = evaluate(policy, allocation)
    assert not failures
    assert round(rows[0][4], 2) == 12.0


def test_budget_evaluation_flags_forecast_over_budget():
    policy = {
        "forecast_multiplier": 1.2,
        "team_budgets": {"platform": 100.0},
    }
    allocation = {"records": [{"team": "platform", "cost": 90.0}]}
    _, failures = evaluate(policy, allocation)
    assert failures == ["platform"]
