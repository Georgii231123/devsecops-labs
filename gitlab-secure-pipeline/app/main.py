from __future__ import annotations

import hashlib
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8080


def sha256_text(value: str) -> str:
    """Return a SHA-256 digest for a text value."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Handler(BaseHTTPRequestHandler):
    server_version = ""
    sys_version = ""

    def _send_json(self, status: HTTPStatus, payload: dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        if self.path.startswith("/hash?value="):
            value = self.path.removeprefix("/hash?value=")
            self._send_json(HTTPStatus.OK, {"sha256": sha256_text(value)})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
