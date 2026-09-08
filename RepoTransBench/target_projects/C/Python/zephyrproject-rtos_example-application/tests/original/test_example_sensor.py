import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.sensor.example_sensor import example_sensor_read

def test_example_sensor_read():
    val = example_sensor_read()
    assert val == 42
    print("test_example_sensor_read: PASS")

# Pytest automatically discovers functions starting with 'test_'.
# We keep this for parity with the C output's final print statement.
def test_example_sensor_all_pass_message():
    print("test_example_sensor: ALL PASS")
    assert True