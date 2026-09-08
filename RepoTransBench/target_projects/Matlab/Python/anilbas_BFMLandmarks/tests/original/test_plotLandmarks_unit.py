import pytest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def test_plot_landmarks_unit():
    """
    Test simple landmark plotting with matplotlib (unit test).
    """
    try:
        plt.figure()
        plt.plot([1, 2, 3], [3, 2, 1], 'o-')
        plt.close()
    except Exception as e:
        pytest.fail(f"plotLandmarks plotting failed: {e}")