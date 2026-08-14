import base64
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

SERVICES = {
    "loki": "http://127.0.0.1:3100/ready",
    "tempo": "http://127.0.0.1:3200/ready",
    "mimir": "http://127.0.0.1:9009/ready",
    "grafana": "http://127.0.0.1:3000/api/health",
}


def request(method, url, payload=None, headers=None, timeout=5):
    data = json.dumps(payload).encode() if payload is not None else None
    req_headers = {"Content-Type": "application/json"} if data else {}
    req_headers.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type and raw:
            return json.loads(raw)
        return raw.decode()


def wait(name, url, attempts=90):
    last_error = None
    for _ in range(attempts):
        try:
            request("GET", url)
            return
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"{name} did not become ready: {last_error}")


for service, url in SERVICES.items():
    wait(service, url)

now = time.time_ns()
message = "portfolio-observability-smoke"
request(
    "POST",
    "http://127.0.0.1:3100/loki/api/v1/push",
    {"streams": [{"stream": {"job": "smoke"}, "values": [[str(now), message]]}]},
)

query = urllib.parse.urlencode(
    {
        "query": '{job="smoke"}',
        "start": str(now - 60_000_000_000),
        "end": str(now + 60_000_000_000),
        "limit": "20",
    }
)
for _ in range(20):
    result = request("GET", f"http://127.0.0.1:3100/loki/api/v1/query_range?{query}")
    encoded = json.dumps(result)
    if message in encoded:
        break
    time.sleep(1)
else:
    raise RuntimeError("Loki accepted the smoke log but it was not queryable")

mimir = request(
    "GET",
    "http://127.0.0.1:9009/prometheus/api/v1/query?query=vector%281%29",
)
if mimir.get("status") != "success":
    raise RuntimeError("Mimir Prometheus query API did not return success")

auth = base64.b64encode(b"admin:admin").decode()
datasources = request(
    "GET",
    "http://127.0.0.1:3000/api/datasources",
    headers={"Authorization": f"Basic {auth}"},
)
names = {item["name"] for item in datasources}
required = {"Loki", "Tempo", "Mimir"}
if not required.issubset(names):
    raise RuntimeError(f"Grafana data sources missing: {sorted(required - names)}")

report = {
    "ready": sorted(SERVICES),
    "grafana_datasources": sorted(names & required),
    "loki_write_read": True,
    "mimir_query_api": True,
    "tempo_ready": True,
}
artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)
(artifacts / "stack-health.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
