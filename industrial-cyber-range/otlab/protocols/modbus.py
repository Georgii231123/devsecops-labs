from __future__ import annotations

import struct
from dataclasses import dataclass


class ModbusFrameError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ModbusRequest:
    transaction_id: int
    unit_id: int
    function_code: int
    payload: bytes


def build_request(transaction_id: int, unit_id: int, function_code: int, payload: bytes) -> bytes:
    pdu = bytes([function_code]) + payload
    length = 1 + len(pdu)
    return struct.pack(">HHHB", transaction_id, 0, length, unit_id) + pdu


def parse_request(frame: bytes) -> ModbusRequest:
    if len(frame) < 8:
        raise ModbusFrameError("frame is shorter than MBAP header plus function code")
    transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", frame[:7])
    if protocol_id != 0:
        raise ModbusFrameError("unsupported protocol identifier")
    if length != len(frame) - 6:
        raise ModbusFrameError("MBAP length does not match frame size")
    return ModbusRequest(transaction_id, unit_id, frame[7], frame[8:])


def build_response(request: ModbusRequest, function_code: int, payload: bytes) -> bytes:
    return build_request(request.transaction_id, request.unit_id, function_code, payload)


def build_exception(request: ModbusRequest, code: int) -> bytes:
    return build_response(request, request.function_code | 0x80, bytes([code]))
