import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8001")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/request")
def make_request():
    response = requests.get(f"{BACKEND_URL}/work", timeout=3)
    response.raise_for_status()
    return jsonify({"frontend": "ok", "backend": response.json()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
