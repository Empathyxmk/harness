import pytest
from src.rosenbrock import rosenbrock

class TestRosenbrockPublic:
    def test_rosenbrock_minimum(self):
        J = rosenbrock(1, 1)
        assert J == 0, "Global minimum should be 0 at (1,1)"

    def test_rosenbrock_near_minimum(self):
        x1, x2 = 1.05, 0.92
        J = rosenbrock(x1, x2)
        assert J > 0, 'Should be above the global minimum.'
        # Value is about 3.33..., so set threshold slightly above:
        assert J < 3.4, 'Should be close to the minimum.'