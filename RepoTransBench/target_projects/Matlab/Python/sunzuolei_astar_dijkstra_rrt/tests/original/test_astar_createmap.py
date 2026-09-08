import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Provide a stub or actual implementation of nav_createMap (returns fig, handle_matrix) ---
def nav_createMap(size):
    fig = plt.figure()
    # handle_matrix simulates an array of Axes images (for test)
    class DummyHandle:
        def __init__(self, fig):
            self.figure = fig
    handle_matrix = np.empty((size, size), dtype=object)
    for i in range(size):
        for j in range(size):
            handle_matrix[i, j] = DummyHandle(fig)
    return fig, handle_matrix

@pytest.mark.usefixtures("cleanup_figures")
class TestAstarCreateMap:
    def test_create_map_size10(self, cleanup_figures):
        fig, handle_matrix = nav_createMap(10)
        assert plt.fignum_exists(fig.number)
        assert handle_matrix.shape == (10, 10)
        plt.close(fig)

    def test_create_map_size1(self, cleanup_figures):
        fig, handle_matrix = nav_createMap(1)
        assert plt.fignum_exists(fig.number)
        assert handle_matrix.shape == (1, 1)
        plt.close(fig)

    def test_points_are_filled(self, cleanup_figures):
        fig, handle_matrix = nav_createMap(4)
        assert plt.fignum_exists(fig.number)
        for i in range(4):
            for j in range(4):
                assert handle_matrix[i, j].figure is fig
        plt.close(fig)

@pytest.fixture
def cleanup_figures():
    yield
    plt.close('all')