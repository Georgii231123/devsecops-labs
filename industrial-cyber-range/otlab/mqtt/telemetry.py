from __future__ import annotations

import asyncio
import json
import os

import paho.mqtt.publish as publish

from otlab.protocols.modbus_client import ModbusClient

TELEMETRY_TOPIC = "plant/plc-01/telemetry"


def publish_snapshot(snapshot: dict[str, object], host: str, port: int) -> None:
    publish.single(
        TELEMETRY_TOPIC,
        payload=json.dumps(snapshot, sort_keys=True),
        hostname=host,
        port=port,
        qos=0,
        retain=False,
    )


async def _read_snapshot(client: ModbusClient) -> dict[str, object]:
    process = await client.read_holding_registers(0, 2)
    controls = await client.read_holding_registers(10, 3)
    return {
        "tank_level_pct": process[0] / 10.0,
        "pressure_bar": process[1] / 100.0,
        "pump_speed_pct": controls[0],
        "relief_valve_open": bool(controls[1]),
        "safe_state": bool(controls[2]),
    }


async def _main() -> None:
    modbus_host = os.getenv("OTLAB_MODBUS_HOST", "127.0.0.1")
    modbus_port = int(os.getenv("OTLAB_MODBUS_PORT", "1502"))
    mqtt_host = os.getenv("OTLAB_MQTT_HOST", "127.0.0.1")
    mqtt_port = int(os.getenv("OTLAB_MQTT_PORT", "1883"))
    client = ModbusClient(modbus_host, modbus_port)

    while True:
        try:
            snapshot = await _read_snapshot(client)
            await asyncio.to_thread(publish_snapshot, snapshot, mqtt_host, mqtt_port)
        except (OSError, RuntimeError):
            pass
        await asyncio.sleep(2.0)


if __name__ == "__main__":
    asyncio.run(_main())
