package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PerformanceTest {

    @Test
    void testLargeSumPerformance() {
        int n = 1000000; // 1 million
        List<Integer> biglist = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            biglist.add(i);
        }
        long start = System.currentTimeMillis();
        long sum = biglist.stream().mapToLong(Integer::longValue).sum();
        long took = System.currentTimeMillis() - start;
        assertEquals((n - 1L) * n / 2, sum);
        assertTrue(took < 3000, "Performance: summing 1 million ints should be fast, got "+took+"ms!");
    }
}