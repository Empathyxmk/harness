import pytest
from src.rosenbrock import rosenbrock

class TestRosenbrock:
    def test_rosenbrock_at_minimum(self):
        # At global minimum (1,1)
        x1, x2 = 1, 1
        J = rosenbrock(x1, x2)
        assert J == 0, 'Value at minimum (1,1) should be 0.'

    def test_rosenbrock_at_negative_values(self):
        x1, x2 = -1, 1
        J = rosenbrock(x1, x2)
        expectedJ = 4
        assert J == expectedJ, 'Value at (-1,1) should be 4.'

    def test_rosenbrock_at_large_values(self):
        x1, x2 = 10, 100
        J = rosenbrock(x1, x2)
        expectedJ = 81
        assert J == expectedJ, 'Value at (10,100) should be 81.'

    def test_rosenbrock_at_zero(self):
        x1, x2 = 0, 0
        J = rosenbrock(x1, x2)
        expectedJ = 1
        assert J == expectedJ, 'Value at (0,0) should be 1.'