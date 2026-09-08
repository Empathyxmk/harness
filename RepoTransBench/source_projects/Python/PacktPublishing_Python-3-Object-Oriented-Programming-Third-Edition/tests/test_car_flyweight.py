import pytest
from Chapter11 import car_flyweight

def test_carmodel_singleton_behavior():
    m1 = car_flyweight.CarModel("Sedan", air=True)
    m2 = car_flyweight.CarModel("Sedan", air=False)
    assert m1 is m2
    assert m1.model_name == "Sedan"
    # Should have air as True, as set in first instance
    assert m1.air
    # test attributes
    assert m1.alloy_wheels is False
    m3 = car_flyweight.CarModel("Coupé", air=False, tilt=True)
    assert m3 is not m1
    assert m3.tilt
    assert not m3.air

def test_carmodel_check_serial_output(capsys):
    m = car_flyweight.CarModel("X", power_locks=True)
    m.check_serial("XYZ-123")
    out = capsys.readouterr().out
    assert "XYZ-123" in out and "X" in out

def test_car_check_serial_delegates(capsys):
    m = car_flyweight.CarModel("TestModel")
    c = car_flyweight.Car(m, "Red", 555)
    c.check_serial()
    out = capsys.readouterr().out
    assert "555" in out

def test_car_attributes():
    m = car_flyweight.CarModel("Z")
    c = car_flyweight.Car(m, "Blue", 999)
    assert c.model is m
    assert c.color == "Blue"
    assert c.serial == 999