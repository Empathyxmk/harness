import pytest

class FakeView:
    def __init__(self, left=0, top=0, width=0, height=0):
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    def getLeft(self):
        return self._left

    def getTop(self):
        return self._top

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

class FakeViewGroup:
    def __init__(self, children):
        self._children = children

    def getChildCount(self):
        return len(self._children)

    def getChildAt(self, idx):
        return self._children[idx]

class Animator:
    def __init__(self):
        self._anim = True

# Static methods to simulate "ExpandAnimationUtils"
class ExpandAnimationUtils:
    @staticmethod
    def build(view_group, pivotX, pivotY, fraction, duration, delay):
        # Simulate the Java setup: create 2 children * 2 = 4 anim, plus 1 alpha = 5
        count = view_group.getChildCount() * 2 + 1
        return [Animator() for _ in range(count)]

    @staticmethod
    def buildReversed(view_group, pivotX, pivotY, fraction, duration, delay):
        count = view_group.getChildCount() * 2 + 1
        return [Animator() for _ in range(count)]

@pytest.fixture
def fake_view_group(mocker):
    child1 = mocker.Mock(spec=FakeView)
    child2 = mocker.Mock(spec=FakeView)
    child1.getLeft.return_value = 10
    child1.getTop.return_value = 20
    child1.getWidth.return_value = 30
    child1.getHeight.return_value = 40
    child2.getLeft.return_value = 100
    child2.getTop.return_value = 200
    child2.getWidth.return_value = 50
    child2.getHeight.return_value = 60

    child_list = [child1, child2]

    vg = mocker.Mock(spec=FakeViewGroup)
    vg.getChildCount.return_value = 2
    vg.getChildAt.side_effect = lambda idx: child_list[idx]
    return vg

def test_build(fake_view_group):
    pivotX = 50
    pivotY = 60
    fraction = 0.5
    duration = 300
    delay = 50

    animators = ExpandAnimationUtils.build(fake_view_group, pivotX, pivotY, fraction, duration, delay)
    assert len(animators) == 5
    for i in range(4):
        assert animators[i] is not None
    assert animators[4] is not None

def test_build_reversed(fake_view_group):
    pivotX = 30
    pivotY = 90
    fraction = 0.3
    duration = 400
    delay = 20

    animators = ExpandAnimationUtils.buildReversed(fake_view_group, pivotX, pivotY, fraction, duration, delay)
    assert len(animators) == 5
    for a in animators:
        assert a is not None