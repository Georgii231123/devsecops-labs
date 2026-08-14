import struct

import pytest

from otlab.protocols.modbus import ModbusFrameError, build_request, parse_request


def test_modbus_frame_round_trip() -> None:
    frame = build_request(7, 1, 3, struct.pack(">HH", 0, 2))
    request = parse_request(frame)
    assert request.transaction_id == 7
    assert request.unit_id == 1
    assert request.function_code == 3
    assert request.payload == struct.pack(">HH", 0, 2)


def test_modbus_rejects_wrong_protocol_id() -> None:
    frame = bytearray(build_request(1, 1, 3, struct.pack(">HH", 0, 1)))
    frame[2:4] = b"\x00\x01"
    with pytest.raises(ModbusFrameError):
        parse_request(bytes(frame))
