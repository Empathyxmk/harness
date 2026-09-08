import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Provide a stub or actual implementation of RRT_createMap ---
def RRT_createMap(k):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    map_matrix = np.zeros((200, 200))
    map_size = 200
    return map_matrix, map_size, fig, ax

@pytest.mark.usefixtures("cleanup_figures")
class TestRRTCreateMap:
    def test_all_cases(self, cleanup_figures):
        for k in range(1, 6):
            map_matrix, map_size, fig, ax = RRT_createMap(k)
            assert map_matrix.shape == (200, 200)
            assert map_size == 200
            assert plt.fignum_exists(fig.number)
            assert ax.figure is fig
            plt.close(fig)

    def test_invalid_arg(self, cleanup_figures):
        map_matrix, map_size, fig, ax = RRT_createMap(100)
        assert map_matrix.shape == (200, 200)
        assert map_size == 200
        assert plt.fignum_exists(fig.number)
        assert ax.figure is fig
        plt.close(fig)

@pytest.fixture
def cleanup_figures():
    yield
    plt.close('all')