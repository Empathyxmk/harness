import pytest

def import_state():
    from src.Behavioral.State import TrafficLight
    return TrafficLight

def test_initial_state_sign_and_after_one_change():
    TrafficLight = import_state()
    light = TrafficLight()
    assert light.sign() == 'GO'
    light.change()
    assert light.sign() == 'STOP'

def test_after_three_changes_cycles_back_to_go():
    TrafficLight = import_state()
    light = TrafficLight()
    light.change()
    light.change()
    light.change()
    assert light.sign() == 'GO'

def test_full_cycle_through_states_with_explicit_check():
    TrafficLight = import_state()
    light = TrafficLight()
    assert light.sign() == 'GO'
    light.change()
    assert light.sign() == 'STOP'
    light.change()
    assert light.sign() == 'STEADY'
    light.change()
    assert light.sign() == 'GO'