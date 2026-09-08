package com.packtpublishing.publictests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestPytestStatsTest {
    int[] values;

    @BeforeEach
    void setup() {
        values = new int[]{5,10,15};
    }

    @Test
    void testSum() {
        int sum = 0;
        for (int v : values) sum += v;
        assertEquals(30, sum);
    }

    @Test
    void testMax() {
        int max = values[0];
        for (int v : values) if (v > max) max = v;
        assertEquals(15, max);
    }
}