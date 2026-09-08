package com.nathanrooy.particle;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PsoTest {

    @Test
    public void testMinimizeWithSphereFunction() {
        double[] x0 = {1.0, 2.0};
        double[][] bounds = {{-5, 5}, {-5, 5}};
        Object[] result = PsoSimple.minimize(CostFunctions::sphere, x0, bounds, 4, 15, false);
        double err = (double) result[0];
        @SuppressWarnings("unchecked")
        List<Double> pos = (List<Double>) result[1];
        assertTrue(err <= CostFunctions.sphere(x0));
        assertEquals(x0.length, pos.size());
    }
}