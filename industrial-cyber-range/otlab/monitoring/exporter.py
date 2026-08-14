from __future__ import annotations

import asyncio
import os

from prometheus_client import Gauge, start_http_server

from otlab.protocols.modbus_client import ModbusClient

LEVEL = Gauge("otlab_plc_tank_level_percent", "Tank level read from PLC")
PRESSURE = Gauge("otlab_plc_pressure_bar", "Pressure read from PLC")
PUMP = Gauge("otlab_plc_pump_speed_percent", "Pump speed read from PLC")
VALVE = Gauge("otlab_plc_relief_valve_open", "Relief valve state read from PLC")
SAFE = Gauge("otlab_plc_safe_state", "Safe state read from PLC")
SCRAPE_OK = Gauge("otlab_plc_exporter_read_ok", "Whether the most recent PLC read succeeded")


async def _main() -> None:
    host = os.getenv("OTLAB_MODBUS_HOST", "127.0.0.1")
    port = int(os.getenv("OTLAB_MODBUS_PORT", "1502"))
    metrics_port = int(os.getenv("OTLAB_METRICS_PORT", "9102"))
    start_http_server(metrics_port)
    client = ModbusClient(host, port)

    while True:
        try:
            process = await client.read_holding_registers(0, 2)
            controls = await client.read_holding_registers(10, 3)
            LEVEL.set(process[0] / 10.0)
            PRESSURE.set(process[1] / 100.0)
            PUMP.set(controls[0])
            VALVE.set(controls[1])
            SAFE.set(controls[2])
            SCRAPE_OK.set(1)
        except (OSError, RuntimeError):
            SCRAPE_OK.set(0)
        await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(_main())
