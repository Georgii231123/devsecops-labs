import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def evaluate(policy, allocation):
    observed = {team: 0.0 for team in policy["team_budgets"]}
    for record in allocation["records"]:
        team = record["team"]
        if team not in observed:
            raise ValueError(f"allocation contains team without budget: {team}")
        observed[team] += float(record["cost"])

    rows = []
    failures = []
    multiplier = float(policy["forecast_multiplier"])
    for team, budget in policy["team_budgets"].items():
        forecast = observed[team] * multiplier
        headroom = float(budget) - forecast
        rows.append((team, observed[team], forecast, float(budget), headroom))
        if forecast > float(budget):
            failures.append(team)
    return rows, failures


def main():
    policy = json.loads((ROOT / "policy.json").read_text())
    allocation = json.loads((ROOT / "data" / "allocation.json").read_text())
    rows, failures = evaluate(policy, allocation)

    currency = policy["currency"]
    lines = [
        "# FinOps budget report",
        "",
        f"Period: `{allocation['period']}`  ",
        f"Forecast multiplier: `{policy['forecast_multiplier']}`",
        "",
        f"| Team | Observed {currency} | Forecast {currency} | Budget {currency} | Headroom {currency} |",
        "|---|---:|---:|---:|---:|",
    ]
    for team, observed, forecast, budget, headroom in rows:
        lines.append(
            f"| {team} | {observed:.2f} | {forecast:.2f} | {budget:.2f} | {headroom:.2f} |"
        )

    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    (artifacts / "finops-report.md").write_text("\n".join(lines) + "\n")

    if failures:
        raise SystemExit("Forecast exceeds budget for: " + ", ".join(failures))
    print("FinOps budget gate passed")


if __name__ == "__main__":
    main()
