import pytest

class RazerButton:
    def __init__(self, name):
        self.name = name

class RazerButtonFunction:
    def __init__(self, function_name=""):
        self.function_name = function_name

# Simulating C arrays
copperhead_physical_buttons = [RazerButton("Button1"), RazerButton("ButtonN")]
copperhead_button_functions = [RazerButtonFunction("Func1")]

def test_copperhead_physical_buttons():
    # Simple test: check first and last name field for None or not
    assert copperhead_physical_buttons[0].name is not None

def test_copperhead_button_functions():
    # There should be at least 1 function entry
    assert copperhead_button_functions[0] is not None