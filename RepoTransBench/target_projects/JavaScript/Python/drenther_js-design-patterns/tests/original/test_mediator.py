def import_mediator():
    from src.Behavioral.Mediator import TrafficTower, Airplane
    return TrafficTower, Airplane

def test_mediator_pattern():
    TrafficTower, Airplane = import_mediator()
    tower = TrafficTower()
    airplanes = [Airplane(10), Airplane(20), Airplane(30)]
    for airplane in airplanes:
        tower.register(airplane)
    expected_coordinates = [[20, 30], [10, 30], [10, 20]]
    result = [airplane.request_coordinates() for airplane in airplanes]
    assert result == expected_coordinates