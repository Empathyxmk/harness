import math
import pytest

from src.simplex_noise.simplex_noise import SimplexNoise

def test_constructor_edge_cases():
    # Check output is finite for a range of standard usages, using static methods (matching header)
    f1 = SimplexNoise.noise(0.0)
    assert math.isfinite(f1)

    f2 = SimplexNoise.noise(1e6)
    assert math.isfinite(f2)

    f3 = SimplexNoise.noise(123.456, 789.123)
    assert math.isfinite(f3)

    f4 = SimplexNoise.noise(-1e5, 1e6)
    assert math.isfinite(f4)

    f5 = SimplexNoise.noise(1.0, 2.0, 3.0)
    assert math.isfinite(f5)

    f6 = SimplexNoise.noise(-999.0, -2222.0, 5555.0)
    assert math.isfinite(f6)

    # Test non-default params with instance methods (octave, lacunarity, etc)
    noise_custom = SimplexNoise(0.7, 1.5, 5.0, 32.0)
    g1 = noise_custom.noise(5.5, 60.5)
    assert math.isfinite(g1)

    g2 = noise_custom.noise(-7.7, 2.4, -1.0)
    assert math.isfinite(g2)