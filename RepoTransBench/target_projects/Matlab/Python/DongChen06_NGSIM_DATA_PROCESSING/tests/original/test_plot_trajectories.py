import pytest
import numpy as np
from src.ngsim_data_processing.plot_trajectories import plot_trajectories
import matplotlib

def test_plot_trajectories_basic():
    # Basic call with correct vectors
    x = np.linspace(0, 1, 50)
    y = x**2
    plot_trajectories(x, y)

def test_plot_trajectories_size_mismatch():
    # Should raise error when input sizes do not match
    with pytest.raises(ValueError):
        plot_trajectories(np.arange(1, 11), np.arange(1, 9))

def test_plot_trajectories_non_numeric():
    # Should raise error when non-numeric input is given
    with pytest.raises(ValueError):
        plot_trajectories('abc', [1, 2, 3])