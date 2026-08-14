from otlab.plant import ProcessState


def test_process_stays_inside_physical_bounds() -> None:
    state = ProcessState(pump_speed_pct=100)
    for _ in range(200):
        state.step(0.5)
    assert 0 <= state.tank_level_pct <= 100
    assert 0 <= state.pressure_bar <= 10


def test_relief_valve_reduces_pressure_target() -> None:
    closed = ProcessState(pump_speed_pct=80, relief_valve_open=False)
    opened = ProcessState(pump_speed_pct=80, relief_valve_open=True)
    for _ in range(5):
        closed.step(1)
        opened.step(1)
    assert opened.pressure_bar < closed.pressure_bar
