import time
from flask import Flask

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/work")
def work():
    time.sleep(0.05)
    return {"backend": "ok", "operation": "simulated-work"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
