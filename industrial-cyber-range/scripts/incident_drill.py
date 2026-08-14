#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from otlab.incidents import run_scenario

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=["unauthorized-modbus-write", "high-pressure"],
        required=True,
    )
    args = parser.parse_args()
    report = run_scenario(args.scenario)
    output_dir = ROOT / "artifacts"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"{args.scenario}.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Incident drill complete: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
