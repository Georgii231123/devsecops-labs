import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def health_payload():
    return {"service": "reusable-ci-sample", "status": "ok"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/healthz":
            self.send_error(404)
            return
        body = json.dumps(health_payload()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    host = os.getenv("SERVICE_HOST", "127.0.0.1")
    ThreadingHTTPServer((host, 8000), Handler).serve_forever()
