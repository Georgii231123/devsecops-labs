import os
import random
import time

from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)
REQUESTS = Counter("http_requests_total", "HTTP requests", ["method", "path", "status"])
ERRORS = Counter("http_errors_total", "HTTP 5xx responses", ["path"])
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["path"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5),
)
IN_FLIGHT = Gauge("http_requests_in_flight", "Requests currently being handled")


def record(path: str, status: int, started: float) -> None:
    REQUESTS.labels(method="GET", path=path, status=str(status)).inc()
    LATENCY.labels(path=path).observe(time.perf_counter() - started)
    if status >= 500:
        ERRORS.labels(path=path).inc()


@app.get("/")
def index():
    started = time.perf_counter()
    with IN_FLIGHT.track_inprogress():
        payload = {"service": "observability-demo", "environment": os.getenv("APP_ENV", "local")}
        record("/", 200, started)
        return jsonify(payload)


@app.get("/work")
def work():
    started = time.perf_counter()
    with IN_FLIGHT.track_inprogress():
        time.sleep(random.uniform(0.01, 0.25))
        status = 500 if random.random() < 0.03 else 200
        record("/work", status, started)
        return jsonify({"status": "ok" if status == 200 else "error"}), status


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
