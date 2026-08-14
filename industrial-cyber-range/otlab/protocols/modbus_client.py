from __future__ import annotations

import asyncio
import itertools
import struct

from .modbus import build_request, parse_request


class ModbusClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 1502, unit_id: int = 1) -> None:
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self._transactions = itertools.count(1)

    async def _exchange(self, function_code: int, payload: bytes) -> bytes:
        transaction_id = next(self._transactions) % 65535
        reader, writer = await asyncio.open_connection(self.host, self.port)
        try:
            writer.write(build_request(transaction_id, self.unit_id, function_code, payload))
            await writer.drain()
            header = await reader.readexactly(7)
            _, _, length, _ = struct.unpack(">HHHB", header)
            body = await reader.readexactly(length - 1)
            response = parse_request(header + body)
            if response.function_code & 0x80:
                code = response.payload[0] if response.payload else 0
                raise RuntimeError(f"Modbus exception code {code}")
            if response.function_code != function_code:
                raise RuntimeError("unexpected Modbus function code")
            return response.payload
        finally:
            writer.close()
            await writer.wait_closed()

    async def read_holding_registers(self, start: int, quantity: int) -> list[int]:
        payload = await self._exchange(3, struct.pack(">HH", start, quantity))
        byte_count = payload[0]
        raw = payload[1:]
        if byte_count != len(raw) or byte_count != quantity * 2:
            raise RuntimeError("invalid Modbus read response length")
        return list(struct.unpack(">" + "H" * quantity, raw))

    async def write_single_register(self, address: int, value: int) -> None:
        expected = struct.pack(">HH", address, value)
        payload = await self._exchange(6, expected)
        if payload != expected:
            raise RuntimeError("write echo mismatch")
