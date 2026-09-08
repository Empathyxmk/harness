import pytest

def import_state():
    from src.Behavioral.State import TrafficLight
    return TrafficLight

@pytest.fixture
def traffic_light():
    TrafficLight = import_state()
    return TrafficLight()

def test_initial_state_is_green(traffic_light):
    assert traffic_light.sign() == 'GO'

def test_cycles_green_red_yellow_green(traffic_light):
    traffic_light.change()
    assert traffic_light.sign() == 'STOP'
    traffic_light.change()
    assert traffic_light.sign() == 'STEADY'
    traffic_light.change()
    assert traffic_light.sign() == 'GO'

def test_multiple_full_cycles_work_correctly(traffic_light):
    for _ in range(9):
        traffic_light.change()
    assert traffic_light.sign() == 'GO'