import pytest
import numpy as np
from src.ngsim_data_processing.plot_trajectories import plot_trajectories

def test_plot_trajectories_public_diff_vectors():
    # Different vectors: sin and cos, increased points
    xx = np.linspace(-2, 2, 60)
    yy = np.sin(xx) * np.cos(xx)
    plot_trajectories(xx, yy)

def test_plot_trajectories_public_empty_input():
    # Error: test with empty input (different from existing test)
    with pytest.raises(ValueError):
        plot_trajectories([], [])

def test_plot_trajectories_public_non_numeric_second_arg():
    # Error: non-numeric input as second argument (different type)
    with pytest.raises(ValueError):
        plot_trajectories(np.arange(6), ['a', 'b', 'c', 'd', 'e', 'f'])