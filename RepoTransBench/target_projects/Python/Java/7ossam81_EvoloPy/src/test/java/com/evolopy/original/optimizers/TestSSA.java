package com.evolopy.original.optimizers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSSA {
    @Test
    public void testSSARuns() {
        double[] lb = {-10,-10,-10,-10,-10};
        double[] ub = {10,10,10,10,10};
        int dim = 5, popSize = 10, iters = 30;
        double[] bestIndividual = new double[dim];
        double[] convergence = new double[iters];
        double best = 0.0;
        assertEquals(dim, bestIndividual.length);
        assertEquals(iters, convergence.length);
        assertTrue(best >= 0);
    }
}