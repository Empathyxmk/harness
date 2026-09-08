import pytest

class RoundStatusImpl:
    def __init__(self):
        self._radius = 0.0
        self._top_left = 0.0
        self._top_right = 0.0
        self._bottom_left = 0.0
        self._bottom_right = 0.0
        self._radius_list = [0.0] * 8

    def setRadius(self, value):
        self._radius = value
        self._radius_list = [value] * 8

    def setTopLeftRadius(self, value):
        self._top_left = value

    def setTopRightRadius(self, value):
        self._top_right = value

    def setBottomRightRadius(self, value):
        self._bottom_right = value

    def setBottomLeftRadius(self, value):
        self._bottom_left = value

    def fillRadius(self):
        self._radius_list = [
            self._top_left, self._top_left,
            self._top_right, self._top_right,
            self._bottom_right, self._bottom_right,
            self._bottom_left, self._bottom_left
        ]

    def getRadius(self):
        return self._radius

    def getTopLeftRadius(self):
        return self._top_left

    def getTopRightRadius(self):
        return self._top_right

    def getBottomRightRadius(self):
        return self._bottom_right

    def getBottomLeftRadius(self):
        return self._bottom_left

    def getRadiusList(self):
        return self._radius_list.copy()

    class RoundStatusBuilder:
        def __init__(self):
            self._m_radius = 0.0
            self._m_top_left = 0.0
            self._m_top_right = 0.0
            self._m_bottom_right = 0.0
            self._m_bottom_left = 0.0

        def setMRadius(self, value):
            self._m_radius = value
            return self

        def setMTopLeftRadius(self, value):
            self._m_top_left = value
            return self

        def setMTopRightRadius(self, value):
            self._m_top_right = value
            return self

        def setMBottomRightRadius(self, value):
            self._m_bottom_right = value
            return self

        def setMBottomLeftRadius(self, value):
            self._m_bottom_left = value
            return self

        def build(self):
            obj = RoundStatusImpl()
            obj.setRadius(self._m_radius)
            obj.setTopLeftRadius(self._m_top_left)
            obj.setTopRightRadius(self._m_top_right)
            obj.setBottomRightRadius(self._m_bottom_right)
            obj.setBottomLeftRadius(self._m_bottom_left)
            obj.fillRadius()
            return obj

def test_default_values():
    impl = RoundStatusImpl()
    assert impl.getRadius() == pytest.approx(0.0, abs=1e-6)
    assert impl.getTopLeftRadius() == pytest.approx(0.0, abs=1e-6)
    assert impl.getTopRightRadius() == pytest.approx(0.0, abs=1e-6)
    assert impl.getBottomRightRadius() == pytest.approx(0.0, abs=1e-6)
    assert impl.getBottomLeftRadius() == pytest.approx(0.0, abs=1e-6)
    radius_list = impl.getRadiusList()
    assert len(radius_list) == 8
    for r in radius_list:
        assert r == pytest.approx(0.0, abs=1e-6)

def test_set_radius():
    impl = RoundStatusImpl()
    impl.setRadius(5.5)
    assert impl.getRadius() == pytest.approx(5.5, abs=1e-6)
    radius_list = impl.getRadiusList()
    for r in radius_list:
        assert r == pytest.approx(5.5, abs=1e-6)

def test_set_individual_radii():
    impl = RoundStatusImpl()
    impl.setRadius(1.0)
    impl.setTopLeftRadius(2.0)
    impl.setTopRightRadius(3.0)
    impl.setBottomRightRadius(4.0)
    impl.setBottomLeftRadius(5.0)
    impl.fillRadius()
    assert impl.getRadius() == pytest.approx(1.0, abs=1e-6)
    assert impl.getTopLeftRadius() == pytest.approx(2.0, abs=1e-6)
    assert impl.getTopRightRadius() == pytest.approx(3.0, abs=1e-6)
    assert impl.getBottomRightRadius() == pytest.approx(4.0, abs=1e-6)
    assert impl.getBottomLeftRadius() == pytest.approx(5.0, abs=1e-6)

    r = impl.getRadiusList()
    assert r[0] == pytest.approx(2.0, abs=1e-6)
    assert r[1] == pytest.approx(2.0, abs=1e-6)
    assert r[2] == pytest.approx(3.0, abs=1e-6)
    assert r[3] == pytest.approx(3.0, abs=1e-6)
    assert r[4] == pytest.approx(4.0, abs=1e-6)
    assert r[5] == pytest.approx(4.0, abs=1e-6)
    assert r[6] == pytest.approx(5.0, abs=1e-6)
    assert r[7] == pytest.approx(5.0, abs=1e-6)

def test_fill_radius():
    impl = RoundStatusImpl()
    impl.setRadius(1.0)
    impl.setTopLeftRadius(2.0)
    impl.setTopRightRadius(3.0)
    impl.setBottomRightRadius(4.0)
    impl.setBottomLeftRadius(5.0)
    impl.setRadius(9.0)
    impl.fillRadius()
    lst = impl.getRadiusList()
    assert lst[0] == pytest.approx(2.0, abs=1e-6)
    assert lst[1] == pytest.approx(2.0, abs=1e-6)
    assert lst[2] == pytest.approx(3.0, abs=1e-6)
    assert lst[3] == pytest.approx(3.0, abs=1e-6)
    assert lst[4] == pytest.approx(4.0, abs=1e-6)
    assert lst[5] == pytest.approx(4.0, abs=1e-6)
    assert lst[6] == pytest.approx(5.0, abs=1e-6)
    assert lst[7] == pytest.approx(5.0, abs=1e-6)

def test_builder_sets_values():
    impl = RoundStatusImpl.RoundStatusBuilder() \
        .setMRadius(1.1) \
        .setMTopLeftRadius(2.2) \
        .setMTopRightRadius(3.3) \
        .setMBottomRightRadius(4.4) \
        .setMBottomLeftRadius(5.5) \
        .build()
    assert impl.getRadius() == pytest.approx(1.1, abs=1e-6)
    assert impl.getTopLeftRadius() == pytest.approx(2.2, abs=1e-6)
    assert impl.getTopRightRadius() == pytest.approx(3.3, abs=1e-6)
    assert impl.getBottomRightRadius() == pytest.approx(4.4, abs=1e-6)
    assert impl.getBottomLeftRadius() == pytest.approx(5.5, abs=1e-6)