package com.packtpublishing.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestStatsTest {

    double mean(int[] nums) {
        if(nums.length==0) throw new IllegalArgumentException("Empty array");
        int sum = 0;
        for(int n: nums) sum+= n;
        return (double)sum/nums.length;
    }

    @Test
    void testMeanPositive() {
        assertEquals(6.0, mean(new int[]{2, 4, 6, 8, 10}));
    }

    @Test
    void testMeanSingle() {
        assertEquals(5.0, mean(new int[]{5}));
    }

    @Test
    void testMeanEmpty() {
        assertThrows(IllegalArgumentException.class, () -> mean(new int[]{}));
    }
}