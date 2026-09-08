import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Provide a stub or actual implementation of RRTPlan for signature and execution ---
def RRTPlan(map_matrix, map_size, start, finish, dist_thresh, step_size, iteration, goal_prob, delay_mode, fig):
    # Just a stub; in real use, call your function
    assert fig is not None
    assert map_matrix.shape == (map_size, map_size)
    return

@pytest.mark.usefixtures("cleanup_figures")
class TestRRTPlan:
    def test_rrtplan_easy_path(self, cleanup_figures):
        map_size = 30
        map_matrix = np.zeros((map_size, map_size))
        fig = plt.figure()
        start = (2, 2)
        finish = (28, 28)
        RRTPlan(map_matrix, map_size, start, finish, 5, 3, 80, 0.5, 1, fig)
        plt.close(fig)

    def test_rrtplan_hard_goalprob(self, cleanup_figures):
        map_size = 20
        map_matrix = np.zeros((map_size, map_size))
        fig = plt.figure()
        start = (5, 5)
        finish = (map_size, map_size)
        RRTPlan(map_matrix, map_size, start, finish, 3, 2, 30, 0.01, 1, fig)
        plt.close(fig)

    def test_rrtplan_obstacle(self, cleanup_figures):
        map_size = 20
        map_matrix = np.zeros((map_size, map_size))
        map_matrix[6:12, 7:18] = 1
        fig = plt.figure()
        start = (1, 1)
        finish = (20, 20)
        RRTPlan(map_matrix, map_size, start, finish, 2, 2, 60, 0.7, 1, fig)
        plt.close(fig)

    def test_rrtplan_delay_modes(self, cleanup_figures):
        map_size = 10
        map_matrix = np.zeros((map_size, map_size))
        fig = plt.figure()
        start = (2, 2)
        finish = (9, 9)
        for mode in range(1, 4):
            RRTPlan(map_matrix, map_size, start, finish, 2, 1, 8, 0.7, mode, fig)
        plt.close(fig)

@pytest.fixture
def cleanup_figures():
    yield
    plt.close('all')