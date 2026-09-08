import numpy as np
from src.GA import GA

def test_public_GA():
    numTasks = 9
    tasks = np.random.randint(900_000, 3_000_001, size=(numTasks,))
    N = numTasks
    pop_size = 30
    iteration = 10
    BestSolution, BestFitness = GA(tasks, N, pop_size, iteration)
    assert len(BestSolution) == N, 'BestSolution size mismatch'
    assert isinstance(BestFitness, (int, float, np.floating, np.integer)) and np.isscalar(BestFitness), 'BestFitness should be a scalar number'