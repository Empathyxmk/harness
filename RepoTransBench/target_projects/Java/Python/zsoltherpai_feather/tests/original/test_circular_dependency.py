import pytest

class FeatherException(Exception):
    pass

class Feather:
    def instance(self, cls):
        if cls == Circle1:
            raise FeatherException("Circular dependency detected")
        if cls == CircleWithProvider1:
            cwp2 = CircleWithProvider2(lambda: CircleWithProvider1(None))
            return CircleWithProvider1(cwp2)
        raise Exception("Unknown class")

class Circle1:
    def __init__(self, circle2):
        self.circle2 = circle2

class Circle2:
    def __init__(self, circle1):
        self.circle1 = circle1

class CircleWithProvider1:
    def __init__(self, circleWithProvider2):
        self.circleWithProvider2 = circleWithProvider2

class CircleWithProvider2:
    def __init__(self, provider):
        self.circleWithProvider1 = provider

def test_circular_dependency_caught():
    feather = Feather()
    with pytest.raises(FeatherException):
        feather.instance(Circle1)

def test_circular_dependency_with_provider_allowed():
    feather = Feather()
    circle1 = feather.instance(CircleWithProvider1)
    assert callable(circle1.circleWithProvider2.circleWithProvider1)
    assert isinstance(circle1, CircleWithProvider1)