import pytest

# We assume Strategy.py module exists and contains classes: Bus, Taxi, PersonalCar, Commute

def import_strategy():
    # Assume presence of Strategy.py in src/Behavioral/Strategy.py
    from src.Behavioral.Strategy import Bus, Taxi, PersonalCar, Commute
    return Bus, Taxi, PersonalCar, Commute

def test_travel_by_bus():
    Bus, _, _, Commute = import_strategy()
    bus = Bus()
    commute = Commute()
    assert commute.travel(bus) == 10

def test_travel_by_taxi():
    _, Taxi, _, Commute = import_strategy()
    taxi = Taxi()
    commute = Commute()
    assert commute.travel(taxi) == 5

def test_travel_by_personal_car():
    _, _, PersonalCar, Commute = import_strategy()
    car = PersonalCar()
    commute = Commute()
    assert commute.travel(car) == 3

def test_travel_without_transport_throws():
    _, _, _, Commute = import_strategy()
    commute = Commute()
    with pytest.raises(Exception):
        commute.travel(None)