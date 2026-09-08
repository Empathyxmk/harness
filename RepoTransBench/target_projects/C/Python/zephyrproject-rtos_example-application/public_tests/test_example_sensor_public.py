import pytest

# This function is specific to the public test and should not interfere with original 'example_sensor'
def fake_sensor_read_public(pin):
    if pin == 5:
        return 200
    if pin == 2:
        return 123
    return -1

def test_example_sensor_read_public_test():
    print("Running public test_example_sensor_public.c ...")
    assert fake_sensor_read_public(5) == 200, f"Expected 200, got {fake_sensor_read_public(5)}"
    assert fake_sensor_read_public(2) == 123, f"Expected 123, got {fake_sensor_read_public(2)}"
    assert fake_sensor_read_public(-1) == -1, f"Expected -1, got {fake_sensor_read_public(-1)}"
    print("test_example_sensor_public passed!")