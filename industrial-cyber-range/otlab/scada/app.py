from __future__ import annotations

import asyncio
import os

from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest

from otlab.protocols.modbus_client import ModbusClient

REQUESTS = Counter("otlab_scada_requests_total", "SCADA HTTP requests", ["endpoint", "status"])
LEVEL = Gauge("otlab_tank_level_percent", "Tank level percent")
PRESSURE = Gauge("otlab_pressure_bar", "Process pressure in bar")
PUMP = Gauge("otlab_pump_speed_percent", "Pump speed percent")
SAFE = Gauge("otlab_safe_state", "Whether the process is in safe state")


async def _read_state(host: str, port: int) -> dict[str, object]:
    client = ModbusClient(host, port)
    process = await client.read_holding_registers(0, 2)
    controls = await client.read_holding_registers(10, 3)
    state = {
        "tank_level_pct": process[0] / 10.0,
        "pressure_bar": process[1] / 100.0,
        "pump_speed_pct": controls[0],
        "relief_valve_open": bool(controls[1]),
        "safe_state": bool(controls[2]),
    }
    LEVEL.set(float(state["tank_level_pct"]))
    PRESSURE.set(float(state["pressure_bar"]))
    PUMP.set(float(state["pump_speed_pct"]))
    SAFE.set(int(bool(state["safe_state"])))
    return state


def create_app() -> Flask:
    app = Flask(__name__)
    modbus_host = os.getenv("OTLAB_MODBUS_HOST", "127.0.0.1")
    modbus_port = int(os.getenv("OTLAB_MODBUS_PORT", "1502"))

    @app.get("/healthz")
    def healthz() -> tuple[dict[str, str], int]:
        REQUESTS.labels("healthz", "200").inc()
        return {"status": "ok"}, 200

    @app.get("/api/state")
    def state() -> tuple[Response, int] | Response:
        try:
            snapshot = asyncio.run(_read_state(modbus_host, modbus_port))
        except (OSError, RuntimeError):
            REQUESTS.labels("state", "503").inc()
            return jsonify({"status": "unavailable"}), 503
        REQUESTS.labels("state", "200").inc()
        return jsonify(snapshot)

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app


if __name__ == "__main__":
    bind = os.getenv("SCADA_BIND", "127.0.0.1")
    port = int(os.getenv("SCADA_PORT", "8080"))
    create_app().run(host=bind, port=port, debug=False)
