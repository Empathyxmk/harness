package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestStatsTest {
    static double mean(int[] values) {
        if (values.length == 0) throw new IllegalArgumentException("empty array");
        int sum = 0;
        for (int v : values) sum += v;
        return (double)sum / values.length;
    }

    @Test
    void testMeanBasic() {
        assertEquals(3.0, mean(new int[]{1,2,3,4,5}));
    }

    @Test
    void testMeanNegative() {
        assertEquals(-1.5, mean(new int[]{-1, -2}));
    }

    @Test
    void testMeanEmpty() {
        assertThrows(IllegalArgumentException.class, () -> mean(new int[]{}));
    }
}