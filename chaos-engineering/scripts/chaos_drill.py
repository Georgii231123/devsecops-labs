import json
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

API = "http://127.0.0.1:8474"
PROXY = "http://127.0.0.1:8666"


def request(method, url, payload=None, timeout=3):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        return json.loads(raw) if raw else None


def wait_url(url, attempts=40):
    last_error = None
    for _ in range(attempts):
        try:
            return request("GET", url)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"{url} did not become ready: {last_error}")


def timed_health():
    start = time.perf_counter()
    payload = request("GET", f"{PROXY}/healthz", timeout=5)
    elapsed = time.perf_counter() - start
    if payload.get("status") != "ok":
        raise RuntimeError("unexpected API response")
    return elapsed


wait_url(f"{API}/version")
proxies = request("GET", f"{API}/proxies")
if "api" in proxies:
    request("DELETE", f"{API}/proxies/api")

request(
    "POST",
    f"{API}/proxies",
    {
        "name": "api",
        "listen": "0.0.0.0:8666",
        "upstream": "app:8000",
        "enabled": True,
    },
)
wait_url(f"{PROXY}/healthz")

baseline = min(timed_health() for _ in range(3))
request(
    "POST",
    f"{API}/proxies/api/toxics",
    {
        "name": "latency",
        "type": "latency",
        "stream": "downstream",
        "toxicity": 1.0,
        "attributes": {"latency": 1200, "jitter": 0},
    },
)
fault_latency = timed_health()
if fault_latency < baseline + 0.9:
    raise RuntimeError(
        f"latency fault was not observable: baseline={baseline:.3f}s fault={fault_latency:.3f}s"
    )

request("DELETE", f"{API}/proxies/api/toxics/latency")
recovered_latency = min(timed_health() for _ in range(3))
if recovered_latency > baseline + 0.6:
    raise RuntimeError(
        f"latency did not recover: baseline={baseline:.3f}s recovered={recovered_latency:.3f}s"
    )

subprocess.run(["docker", "compose", "restart", "app"], check=True)
wait_url(f"{PROXY}/healthz", attempts=45)

report = {
    "hypothesis": "latency is observable and the service path recovers after fault removal and backend restart",
    "baseline_seconds": round(baseline, 3),
    "fault_seconds": round(fault_latency, 3),
    "recovered_seconds": round(recovered_latency, 3),
    "backend_restart_recovered": True,
}
artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)
(artifacts / "chaos-report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
