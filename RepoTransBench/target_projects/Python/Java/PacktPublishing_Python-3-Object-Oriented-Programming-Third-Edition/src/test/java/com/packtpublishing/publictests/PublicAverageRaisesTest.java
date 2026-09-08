package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicAverageRaisesTest {
    static double average(double[] values) {
        if (values.length == 0) throw new IllegalArgumentException("Empty");
        double sum = 0.0;
        for (double v : values) sum += v;
        return sum / values.length;
    }

    @Test
    void testAverageSimple() {
        double[] vals = {1, 2, 3};
        assertEquals(2.0, average(vals));
    }

    @Test
    void testAverageSingle() {
        assertEquals(5.0, average(new double[]{5.0}));
    }

    @Test
    void testAverageNegative() {
        assertEquals(-1.0, average(new double[]{-1.0}));
    }

    @Test
    void testAverageEmptyThrows() {
        assertThrows(IllegalArgumentException.class, () -> average(new double[]{}));
    }
}