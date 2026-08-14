import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

MODE_FILE = Path("/state/mode")
LOCK = threading.Lock()
COUNTERS = {"2xx": 0, "5xx": 0}


def current_mode() -> str:
    try:
        value = MODE_FILE.read_text().strip()
    except FileNotFoundError:
        return "healthy"
    return value or "healthy"


def metrics() -> str:
    mode = current_mode()
    with LOCK:
        ok = COUNTERS["2xx"]
        errors = COUNTERS["5xx"]
    failure = 1 if mode == "errors" else 0
    return "\n".join(
        [
            "# HELP app_requests_total Requests handled by status class.",
            "# TYPE app_requests_total counter",
            f'app_requests_total{{status="2xx"}} {ok}',
            f'app_requests_total{{status="5xx"}} {errors}',
            "# HELP app_failure_mode Whether the service is in the injected error mode.",
            "# TYPE app_failure_mode gauge",
            f"app_failure_mode {failure}",
            "",
        ]
    )


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status: int, body: str, content_type: str = "text/plain; version=0.0.4") -> None:
        payload = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/metrics":
            self.send_text(200, metrics())
            return
        if self.path == "/healthz":
            self.send_text(200, "ok\n", "text/plain")
            return
        if self.path == "/work":
            mode = current_mode()
            status_class = "5xx" if mode == "errors" else "2xx"
            with LOCK:
                COUNTERS[status_class] += 1
            if status_class == "5xx":
                self.send_text(503, "dependency unavailable\n", "text/plain")
            else:
                self.send_text(200, "work completed\n", "text/plain")
            return
        self.send_text(404, "not found\n", "text/plain")

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    host = os.getenv("SERVICE_HOST", "127.0.0.1")
    ThreadingHTTPServer((host, 8000), Handler).serve_forever()
