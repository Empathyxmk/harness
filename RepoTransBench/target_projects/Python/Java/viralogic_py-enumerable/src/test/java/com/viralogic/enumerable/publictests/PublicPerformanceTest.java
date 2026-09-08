package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicPerformanceTest {

    @Test
    void testSpeedySum() {
        int max = 100000;
        List<Integer> xs = new ArrayList<>();
        for (int i = 0; i < max; i++) xs.add(i);
        long start = System.currentTimeMillis();
        long s = xs.stream().mapToLong(Integer::longValue).sum();
        long took = System.currentTimeMillis() - start;
        assertEquals((max - 1L) * max / 2, s);
        assertTrue(took < 1500, "Public perf: Large sum!");
    }
}