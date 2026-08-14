from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from asyncua import Server

from otlab.protocols.modbus_client import ModbusClient


@dataclass(slots=True)
class OPCUANodes:
    tank_level: object
    pressure: object
    pump_speed: object
    relief_valve: object
    safe_state: object


async def build_server(endpoint: str) -> tuple[Server, OPCUANodes]:
    server = Server()
    await server.init()
    server.set_endpoint(endpoint)
    namespace = await server.register_namespace("urn:otlab:process")
    process = await server.nodes.objects.add_object(namespace, "PumpStation")
    nodes = OPCUANodes(
        tank_level=await process.add_variable(namespace, "TankLevelPct", 45.0),
        pressure=await process.add_variable(namespace, "PressureBar", 2.4),
        pump_speed=await process.add_variable(namespace, "PumpSpeedPct", 35.0),
        relief_valve=await process.add_variable(namespace, "ReliefValveOpen", False),
        safe_state=await process.add_variable(namespace, "SafeState", False),
    )
    return server, nodes


async def update_nodes(nodes: OPCUANodes, values: list[int]) -> None:
    await nodes.tank_level.write_value(values[0] / 10.0)
    await nodes.pressure.write_value(values[1] / 100.0)
    await nodes.pump_speed.write_value(float(values[2]))
    await nodes.relief_valve.write_value(bool(values[3]))
    await nodes.safe_state.write_value(bool(values[4]))


async def _main() -> None:
    endpoint = os.getenv("OTLAB_OPCUA_ENDPOINT", "opc.tcp://127.0.0.1:4840/otlab/server/")
    modbus_host = os.getenv("OTLAB_MODBUS_HOST", "127.0.0.1")
    modbus_port = int(os.getenv("OTLAB_MODBUS_PORT", "1502"))
    server, nodes = await build_server(endpoint)
    client = ModbusClient(modbus_host, modbus_port)

    async with server:
        while True:
            try:
                values = [
                    (await client.read_holding_registers(0, 2))[0],
                    (await client.read_holding_registers(0, 2))[1],
                    (await client.read_holding_registers(10, 3))[0],
                    (await client.read_holding_registers(10, 3))[1],
                    (await client.read_holding_registers(10, 3))[2],
                ]
                await update_nodes(nodes, values)
            except (OSError, RuntimeError):
                pass
            await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(_main())
