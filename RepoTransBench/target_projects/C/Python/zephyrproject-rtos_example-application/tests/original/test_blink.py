import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.blink.gpio_led import gpio_led_on, gpio_led_off

def test_gpio_led_on_normal():
    result = gpio_led_on(1)
    assert result == 0
    print("test_gpio_led_on: PASS")

def test_gpio_led_off_normal():
    result = gpio_led_off(1)
    assert result == 0
    print("test_gpio_led_off: PASS")

def test_gpio_led_on_negative():
    result = gpio_led_on(-1)
    assert result == -1
    print("test_gpio_led_on (negative): PASS")

def test_gpio_led_off_negative():
    result = gpio_led_off(-1)
    assert result == -1
    print("test_gpio_led_off (negative): PASS")

# Pytest automatically discovers functions starting with 'test_'.
# We keep this for parity with the C output's final print statement.
def test_blink_all_pass_message():
    print("test_blink: ALL PASS")
    assert True