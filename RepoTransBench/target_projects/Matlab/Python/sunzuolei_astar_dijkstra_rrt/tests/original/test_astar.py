import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Provide a stub or actual implementation of AStar function here or import from src ---
def AStar(start_x, start_y, end_x, end_y, which_list, fig, obj_map, delay):
    # Stub: Simulate running A* (replace with your implementation or src import)
    assert fig is not None
    assert obj_map is not None
    # Could do some mock plotting for delay, etc.

@pytest.mark.usefixtures("cleanup_figures")
class TestAStar:
    def test_astar_straight(self, cleanup_figures):
        obj = np.ones((10, 10))
        obj_map = obj.copy()
        fig = plt.figure()
        AStar(1, 1, 10, 10, np.zeros((10, 10)), fig, obj_map, 1)
        plt.close(fig)

    def test_astar_same_start_finish(self, cleanup_figures):
        obj = np.ones((5, 5))
        fig = plt.figure()
        AStar(3, 3, 3, 3, np.zeros((5, 5)), fig, obj, 1)
        plt.close(fig)

    def test_astar_delay_modes(self, cleanup_figures):
        obj = np.ones((6, 6))
        fig = plt.figure()
        which_list = np.zeros((6, 6))
        start = (1, 1)
        finish = (6, 6)
        for delay in range(1, 4):
            AStar(start[0], start[1], finish[0], finish[1], which_list, fig, obj, delay)
        plt.close(fig)

@pytest.fixture
def cleanup_figures():
    yield
    plt.close('all')