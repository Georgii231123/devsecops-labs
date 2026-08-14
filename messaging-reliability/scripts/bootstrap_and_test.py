import base64
import http.client
import json
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:15672/api"
AUTH = base64.b64encode(b"lab:lab").decode()


def request(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read()
        return json.loads(body) if body else None


def wait_ready():
    last_error = None
    for _ in range(45):
        try:
            request("GET", "/overview")
            return
        except (urllib.error.URLError, ConnectionError, TimeoutError, http.client.HTTPException) as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"RabbitMQ management API did not become ready: {last_error}")


wait_ready()
request("PUT", "/exchanges/%2F/events", {"type": "topic", "durable": True, "auto_delete": False, "internal": False, "arguments": {}})
request("PUT", "/exchanges/%2F/events.dlx", {"type": "direct", "durable": True, "auto_delete": False, "internal": False, "arguments": {}})
request("PUT", "/queues/%2F/events.q", {"durable": True, "auto_delete": False, "arguments": {"x-queue-type": "quorum", "x-dead-letter-exchange": "events.dlx", "x-dead-letter-routing-key": "dead"}})
request("PUT", "/queues/%2F/events.dlq", {"durable": True, "auto_delete": False, "arguments": {"x-queue-type": "quorum"}})
request("POST", "/bindings/%2F/e/events/q/events.q", {"routing_key": "event.#", "arguments": {}})
request("POST", "/bindings/%2F/e/events.dlx/q/events.dlq", {"routing_key": "dead", "arguments": {}})

published = request("POST", "/exchanges/%2F/events/publish", {"properties": {"delivery_mode": 2}, "routing_key": "event.created", "payload": '{"id":42,"type":"created"}', "payload_encoding": "string"})
if not published or not published.get("routed"):
    raise RuntimeError("message was not routed")

rejected = request("POST", "/queues/%2F/events.q/get", {"count": 1, "ackmode": "reject_requeue_false", "encoding": "auto", "truncate": 50000})
if not rejected:
    raise RuntimeError("source queue did not return the message")

for _ in range(10):
    dead = request("POST", "/queues/%2F/events.dlq/get", {"count": 1, "ackmode": "ack_requeue_false", "encoding": "auto", "truncate": 50000})
    if dead:
        if '"id":42' not in dead[0].get("payload", ""):
            raise RuntimeError("unexpected dead-letter payload")
        print("RabbitMQ quorum/DLQ smoke test passed")
        break
    time.sleep(1)
else:
    raise RuntimeError("dead-letter message was not verified")
