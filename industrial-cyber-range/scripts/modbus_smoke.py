#!/usr/bin/env python3
from __future__ import annotations

import asyncio

from otlab.plc import PLCController
from otlab.protocols.modbus_client import ModbusClient
from otlab.protocols.modbus_server import ModbusTCPServer


async def main() -> None:
    controller = PLCController(allowed_writers={"127.0.0.1"})
    server = ModbusTCPServer(controller, host="127.0.0.1", port=15020, allow_writes=True)
    await server.start()
    try:
        client = ModbusClient("127.0.0.1", 15020)
        initial = await client.read_holding_registers(0, 2)
        assert len(initial) == 2
        await client.write_single_register(10, 55)
        controls = await client.read_holding_registers(10, 3)
        assert controls[0] == 55
        print("Modbus/TCP smoke test: OK")
    finally:
        await server.close()


if __name__ == "__main__":
    asyncio.run(main())
