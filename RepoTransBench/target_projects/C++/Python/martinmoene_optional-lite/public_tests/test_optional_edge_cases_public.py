from src.optional_lite import Optional

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def test_empty_optional():
    o = Optional()
    assert not o.has_value()

def test_value_access():
    o = Optional("hello-public")
    assert o.has_value()
    assert o.value() == "hello-public"

def test_assign_and_reset():
    o = Optional(6.28)
    assert o.has_value()
    o.reset()
    assert not o.has_value()

def test_vector_of_optionals():
    # Simulate a vector of Optional<Point>
    points = [Optional(), Optional()]
    points[0] = Optional(Point(7, 8))
    assert points[0].has_value()
    assert points[0].value().x == 7
    assert points[0].value().y == 8
    assert not points[1].has_value()

def test_emplace():
    op = Optional()
    op.emplace(Point(99, 42))
    assert op.has_value()
    assert op.value().x == 99
    assert op.value().y == 42