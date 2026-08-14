import pytest

from otlab.plc import PLCController, UnauthorizedWrite


def test_unauthorized_writer_is_rejected() -> None:
    plc = PLCController()
    with pytest.raises(UnauthorizedWrite):
        plc.write_register("it-workstation-01", 10, 100)
    assert plc.state.pump_speed_pct == 35
    assert plc.audit[-1].outcome == "rejected"


def test_high_pressure_enters_safe_state() -> None:
    plc = PLCController()
    plc.write_register("engineering-01", 10, 100)
    for _ in range(10):
        plc.tick(1)
        if plc.state.safe_state:
            break
    assert plc.state.safe_state is True
    assert plc.state.pump_speed_pct == 10
    assert plc.state.relief_valve_open is True
