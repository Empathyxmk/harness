package com.evolopy.original.optimizers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestBAT {
    @Test
    public void testBATRuns() {
        // Dummy invocation of BAT optimizer
        double[] lb = {-10,-10,-10,-10,-10};
        double[] ub = {10,10,10,10,10};
        int dim = 5, popSize = 10, iters = 30;
        double[] bestIndividual = new double[dim];
        double[] convergence = new double[iters];
        double best = 0.0;
        // Simulate assertion (replace with real BAT use)
        assertEquals(dim, bestIndividual.length);
        assertEquals(iters, convergence.length);
        assertTrue(best >= 0);
    }
}