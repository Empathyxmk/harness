package com.packtpublishing.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestPytestStatsTest {

    int[] stats;

    @BeforeEach
    void setupStats() {
        stats = new int[]{9, 3, 6};
    }

    @Test
    void testStatsSum() {
        int sum = 0;
        for(int v : stats) sum += v;
        assertEquals(18, sum);
    }

    @Test
    void testStatsMax() {
        int max = stats[0];
        for (int v : stats) if (v > max) max = v;
        assertEquals(9, max);
    }

    @AfterEach
    void teardownStats() {
        stats = null;
    }
}