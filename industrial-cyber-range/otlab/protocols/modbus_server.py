from __future__ import annotations

import asyncio
import os
import struct

from otlab.plc import PLCController

from .modbus import ModbusRequest, build_exception, build_response


class ModbusTCPServer:
    def __init__(
        self,
        controller: PLCController | None = None,
        host: str = "127.0.0.1",
        port: int = 1502,
        allow_writes: bool = False,
    ) -> None:
        self.controller = controller or PLCController(allowed_writers={"127.0.0.1"})
        self.host = host
        self.port = port
        self.allow_writes = allow_writes
        self._server: asyncio.AbstractServer | None = None
        self._ticker: asyncio.Task[None] | None = None

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle_client, self.host, self.port)
        self._ticker = asyncio.create_task(self._tick_process())

    async def close(self) -> None:
        if self._ticker:
            self._ticker.cancel()
            await asyncio.gather(self._ticker, return_exceptions=True)
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _tick_process(self) -> None:
        while True:
            await asyncio.sleep(0.5)
            self.controller.tick(0.5)

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        peer = writer.get_extra_info("peername")
        source = peer[0] if peer else "unknown"
        try:
            while True:
                header = await reader.readexactly(7)
                transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", header)
                if protocol_id != 0 or length < 2:
                    return
                body = await reader.readexactly(length - 1)
                request = ModbusRequest(transaction_id, unit_id, body[0], body[1:])
                writer.write(self._dispatch(request, source))
                await writer.drain()
        except asyncio.IncompleteReadError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    def _dispatch(self, request: ModbusRequest, source: str) -> bytes:
        if request.function_code == 3:
            if len(request.payload) != 4:
                return build_exception(request, 3)
            start, quantity = struct.unpack(">HH", request.payload)
            try:
                values = self.controller.read_registers(start, quantity)
            except (KeyError, ValueError):
                return build_exception(request, 2)
            encoded = b"".join(struct.pack(">H", value) for value in values)
            return build_response(request, 3, bytes([len(encoded)]) + encoded)

        if request.function_code == 6:
            if not self.allow_writes:
                return build_exception(request, 1)
            if len(request.payload) != 4:
                return build_exception(request, 3)
            address, value = struct.unpack(">HH", request.payload)
            try:
                self.controller.write_register(source, address, value)
            except PermissionError:
                return build_exception(request, 1)
            except KeyError:
                return build_exception(request, 2)
            except ValueError:
                return build_exception(request, 3)
            return build_response(request, 6, request.payload)

        return build_exception(request, 1)

    async def serve_forever(self) -> None:
        await self.start()
        assert self._server is not None
        async with self._server:
            await self._server.serve_forever()


async def _main() -> None:
    host = os.getenv("OTLAB_MODBUS_BIND", "127.0.0.1")
    port = int(os.getenv("OTLAB_MODBUS_PORT", "1502"))
    allow_writes = os.getenv("OTLAB_ALLOW_MODBUS_WRITES", "0") == "1"
    server = ModbusTCPServer(host=host, port=port, allow_writes=allow_writes)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(_main())
