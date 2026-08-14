#!/usr/bin/env python3
from __future__ import annotations

import asyncio

from asyncua import Client

from otlab.opcua.server import build_server


async def main() -> None:
    endpoint = "opc.tcp://127.0.0.1:48410/otlab/smoke/"
    server, nodes = await build_server(endpoint)
    await nodes.tank_level.write_value(47.5)
    async with server:
        async with Client(url=endpoint) as client:
            node = client.get_node(nodes.tank_level.nodeid)
            value = await node.read_value()
            assert abs(float(value) - 47.5) < 0.01
    print("OPC UA smoke test: OK")


if __name__ == "__main__":
    asyncio.run(main())
