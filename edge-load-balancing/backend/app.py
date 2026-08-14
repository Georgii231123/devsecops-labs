import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

NAME = os.getenv("BACKEND_NAME", "unknown")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            payload = {"status": "ok", "backend": NAME}
        elif self.path == "/":
            payload = {"backend": NAME, "status": "served"}
        else:
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
