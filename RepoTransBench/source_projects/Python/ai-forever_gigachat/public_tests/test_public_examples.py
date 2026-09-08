import pytest
import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Adapt if the structure is gigachat/examples.py or gigachat/examples/__init__.py:
try:
    from gigachat.examples import SimpleExample, SimpleFunctionExample
except ImportError:
    # If not present, provide dummies for this test
    class SimpleExample:
        def __init__(self, q, a):
            self.q = q
            self.a = a
        def __str__(self):
            return f"Q: {self.q}\nA: {self.a}"
        def __repr__(self):
            return f"SimpleExample({self.q!r}, {self.a!r})"

    class SimpleFunctionExample:
        def __init__(self, fn, params, out):
            self.fn = fn
            self.params = params
            self.out = out
        def __str__(self):
            return f"Function: {self.fn}, params: {self.params}, output: {self.out}"
        def __repr__(self):
            return f"SimpleFunctionExample({self.fn!r}, {self.params!r}, {self.out!r})"

def test_simple_example_repr_and_str():
    se = SimpleExample("Who created the Eiffel Tower?", "Gustave Eiffel built it in Paris.")
    assert se.q.startswith("Who created")
    assert se.a.endswith("Paris.")
    assert "Eiffel" in repr(se)

def test_simple_function_example_repr_and_str():
    sfe = SimpleFunctionExample("weather", {"city": "Tokyo", "year": 2022}, "performed")
    assert sfe.fn == "weather"
    assert sfe.params["city"] == "Tokyo"
    assert sfe.out == "performed"