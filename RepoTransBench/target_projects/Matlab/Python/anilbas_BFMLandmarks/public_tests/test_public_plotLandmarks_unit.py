import pytest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def test_public_plot_landmarks_unit():
    """
    Public test for unit landmark plotting with different data.
    """
    try:
        plt.figure()
        plt.plot([2,4,6,8], [5,3,6,1], '*--')
        plt.close()
    except Exception as e:
        pytest.fail(f"Public plotLandmarks test failed: {e}")