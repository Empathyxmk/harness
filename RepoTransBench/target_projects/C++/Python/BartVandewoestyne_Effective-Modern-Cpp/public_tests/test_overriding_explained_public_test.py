import io
import sys

"""
Test similar overriding logic but with a different derived class,
outputting different strings to verify correct override and polymorphism.
"""

class Shape:
    def name(self):
        return "Shape"

class Circle(Shape):
    def name(self):
        return "Circle"

def test_shape_circle_prints_name(capsys):
    # Simulate std::unique_ptr<Shape> shape_ptr = std::make_unique<Circle>();
    shape_ptr = Circle()
    print(f"Object is: {shape_ptr.name()}")
    captured = capsys.readouterr().out
    assert "Object is: Circle" in captured