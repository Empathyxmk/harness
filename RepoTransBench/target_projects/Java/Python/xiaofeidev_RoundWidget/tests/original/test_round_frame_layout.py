import pytest

class RoundFrameLayout:
    def __init__(self, context, attrs=None):
        self._radius = 0.0
        self._top_left = 0.0
        self._top_right = 0.0
        self._bottom_left = 0.0
        self._bottom_right = 0.0
        self._radius_list = [0.0] * 8

    def setRadius(self, value):
        self._radius = value
        self._radius_list = [value] * 8

    def setTopRightRadius(self, value):
        self._top_right = value
        self._radius_list[2] = value
        self._radius_list[3] = value

    def setTopLeftRadius(self, value):
        self._top_left = value
        self._radius_list[0] = value
        self._radius_list[1] = value

    def setBottomLeftRadius(self, value):
        self._bottom_left = value
        self._radius_list[6] = value
        self._radius_list[7] = value

    def setBottomRightRadius(self, value):
        self._bottom_right = value
        self._radius_list[4] = value
        self._radius_list[5] = value

    def fillRadius(self):
        self._radius_list = [
            self._top_left, self._top_left,
            self._top_right, self._top_right,
            self._bottom_right, self._bottom_right,
            self._bottom_left, self._bottom_left
        ]

    def getRadiusList(self):
        return self._radius_list.copy()

    def getRadius(self):
        return self._radius

    def getTopRightRadius(self):
        return self._top_right

@pytest.fixture
def context():
    return {}

def test_constructor_and_init_minimal(context):
    layout = RoundFrameLayout(context)
    assert layout is not None
    assert isinstance(layout, RoundFrameLayout)
    assert layout.getRadiusList() is not None

def test_constructor_with_attrs(context):
    layout = RoundFrameLayout(context, attrs=None)
    assert layout is not None
    assert layout.getRadiusList() is not None

def test_set_and_get_radius(context):
    layout = RoundFrameLayout(context)
    layout.setRadius(5.0)
    assert layout.getRadius() == pytest.approx(5.0, abs=1e-6)
    layout.setTopRightRadius(2.0)
    assert layout.getTopRightRadius() == pytest.approx(2.0, abs=1e-6)

def test_fill_radius_reflects(context):
    layout = RoundFrameLayout(context)
    layout.setRadius(7.0)
    layout.setTopLeftRadius(1.2)
    layout.setTopRightRadius(2.3)
    layout.setBottomLeftRadius(3.4)
    layout.setBottomRightRadius(4.5)
    layout.fillRadius()
    lst = layout.getRadiusList()
    assert lst[0] == pytest.approx(1.2, abs=1e-4)
    assert lst[2] == pytest.approx(2.3, abs=1e-4)
    assert lst[6] == pytest.approx(3.4, abs=1e-4)
    assert lst[4] == pytest.approx(4.5, abs=1e-4)