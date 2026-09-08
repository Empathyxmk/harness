import pytest

def import_strategy():
    from src.Behavioral.Strategy import Bus, Taxi, PersonalCar, Commute
    return Bus, Taxi, PersonalCar, Commute

def test_travel_by_bus_with_custom_method_simulate_delay():
    Bus, _, _, Commute = import_strategy()
    # Simulate a delay by monkey-patching
    class DelayedBus(Bus):
        def travel_time(self):
            return 14
    bus = DelayedBus()
    commute = Commute()
    assert commute.travel(bus) == 14

def test_travel_by_taxi_simulate_surge_pricing():
    _, Taxi, _, Commute = import_strategy()
    class ExpensiveTaxi(Taxi):
        def travel_time(self):
            return 8
    taxi = ExpensiveTaxi()
    commute = Commute()
    assert commute.travel(taxi) == 8

def test_travel_by_personal_car_heavy_traffic_situation():
    _, _, PersonalCar, Commute = import_strategy()
    class SlowCar(PersonalCar):
        def travel_time(self):
            return 9
    car = SlowCar()
    commute = Commute()
    assert commute.travel(car) == 9

def test_travel_with_invalid_transport_object_with_no_travel_time():
    _, _, _, Commute = import_strategy()
    commute = Commute()
    with pytest.raises(Exception):
        # Pass an object without travel_time
        commute.travel({})