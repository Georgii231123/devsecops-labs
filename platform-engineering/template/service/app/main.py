from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({"service": "__SERVICE_SLUG__", "owner": "__OWNER__"})


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/readyz")
def readyz():
    return jsonify({"status": "ready"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=__PORT__)
