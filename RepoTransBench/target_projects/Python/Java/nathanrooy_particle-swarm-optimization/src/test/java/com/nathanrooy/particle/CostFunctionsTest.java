package com.nathanrooy.particle;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CostFunctions {
    // Simulated "sphere" function as in cost_functions.py
    public static double sphere(int[] x) {
        double sum = 0.0;
        for (int a : x) {
            sum += a * a;
        }
        return sum;
    }
    public static double sphere(double[] x) {
        double sum = 0.0;
        for (double a : x) {
            sum += a * a;
        }
        return sum;
    }
}

public class CostFunctionsTest {

    @Test
    public void testSphereAllZeros() {
        assertEquals(0.0, CostFunctions.sphere(new int[]{0, 0, 0}));
    }

    @Test
    public void testSphereSingleValue() {
        assertEquals(9.0, CostFunctions.sphere(new int[]{3}));
    }

    @Test
    public void testSphereNegativeValues() {
        assertEquals(5.0, CostFunctions.sphere(new int[]{-1, -2}));
    }

    @Test
    public void testSphereMixedValues() {
        assertEquals(14.0, CostFunctions.sphere(new int[]{1, -2, 3}));
    }

    @Test
    public void testSphereEmpty() {
        assertEquals(0.0, CostFunctions.sphere(new int[]{}));
    }

    @Test
    public void testMainGuardDoesNothing() {
        // In Python this would simulate __name__ == "main"; in Java, nothing needed.
        // Just check we can access the class and method.
        assertNotNull(CostFunctions.class);
        assertDoesNotThrow(() -> CostFunctions.sphere(new int[]{}));
    }
}