#!/usr/bin/env python3
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODE = ROOT / "runtime" / "mode"
ARTIFACTS = ROOT / "artifacts"
SERVICE = "http://127.0.0.1:18080"
PROM = "http://127.0.0.1:19090"


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def get(url: str, expected=(200,)) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            status = response.status
            body = response.read().decode()
    except urllib.error.HTTPError as exc:
        status = exc.code
        body = exc.read().decode()
    if status not in expected:
        raise RuntimeError(f"unexpected HTTP {status} for {url}: {body}")
    return status, body


def wait_http(url: str, timeout: float = 45.0) -> None:
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            get(url)
            return
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"timed out waiting for {url}: {last_error}")


def alert_firing(name: str) -> bool:
    _, body = get(f"{PROM}/api/v1/alerts")
    payload = json.loads(body)
    alerts = payload["data"]["alerts"]
    return any(item["labels"].get("alertname") == name and item["state"] == "firing" for item in alerts)


def wait_alert(name: str, firing: bool, timeout: float = 30.0) -> float:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if alert_firing(name) is firing:
            return time.time()
        time.sleep(1)
    raise RuntimeError(f"alert {name} did not reach firing={firing}")


def send_work(count: int, expected_status: int) -> None:
    for _ in range(count):
        status, _ = get(f"{SERVICE}/work", expected=(200, 503))
        if status != expected_status:
            raise RuntimeError(f"expected work HTTP {expected_status}, got {status}")


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    wait_http(f"{SERVICE}/healthz")
    wait_http(f"{PROM}/-/ready")

    MODE.write_text("healthy\n")
    send_work(10, 200)
    baseline_at = time.time()

    incident_started = time.time()
    MODE.write_text("errors\n")
    send_work(20, 503)

    detected_at = wait_alert("ApplicationFailureMode", True)

    remediation_started = time.time()
    MODE.write_text("healthy\n")
    send_work(10, 200)

    recovered_at = wait_alert("ApplicationFailureMode", False)
    _, metrics = get(f"{SERVICE}/metrics")
    if "app_failure_mode 0" not in metrics:
        raise RuntimeError("service metric did not return to healthy mode")

    mtta = round(detected_at - incident_started, 3)
    mttr = round(recovered_at - incident_started, 3)
    repair = round(recovered_at - remediation_started, 3)

    timeline = {
        "scenario": "application-5xx-failure-mode",
        "baseline_at": iso(baseline_at),
        "incident_started_at": iso(incident_started),
        "detected_at": iso(detected_at),
        "remediation_started_at": iso(remediation_started),
        "recovered_at": iso(recovered_at),
        "mtta_seconds": mtta,
        "mttr_seconds": mttr,
        "repair_seconds": repair,
        "result": "recovered",
    }
    (ARTIFACTS / "incident-timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")

    postmortem = f"""# Automated incident postmortem

## Summary

The demo service was deliberately switched into a deterministic HTTP 503 failure mode. Prometheus detected the paging condition and the runbook restored healthy state.

## Impact

Twenty synthetic work requests returned HTTP 503 during the controlled incident window.

## Detection

`ApplicationFailureMode` reached firing state after **{mtta:.3f}s**.

## Root cause

The game-day controller changed the shared runtime mode from `healthy` to `errors`.

## Resolution

The documented remediation restored the mode to `healthy`, after which successful traffic was generated and the paging alert resolved.

## Response metrics

- MTTA: **{mtta:.3f}s**
- MTTR: **{mttr:.3f}s**
- remediation-to-clear: **{repair:.3f}s**

## Follow-up actions

1. Keep the paging alert covered by CI so rule changes cannot silently break detection.
2. Keep remediation steps executable and verification-oriented.
3. Review MTTA/MTTR trends if the scenario becomes slower after platform changes.
"""
    (ARTIFACTS / "postmortem.md").write_text(postmortem)
    print(json.dumps(timeline, indent=2))


if __name__ == "__main__":
    main()
