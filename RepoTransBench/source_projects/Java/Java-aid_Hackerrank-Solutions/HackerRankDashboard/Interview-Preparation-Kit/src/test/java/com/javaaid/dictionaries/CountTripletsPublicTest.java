package com.javaaid.dictionaries;

import static org.junit.Assert.assertEquals;

import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class CountTripletsPublicTest {

    @Test
    public void testCaseRatio2() {
        List<Long> arr = Arrays.asList(2L, 4L, 8L, 16L, 32L, 4L, 8L);
        long r = 2L;
        // 2,4,8; 4,8,16; 8,16,32 etc.
        assertEquals(6, CountTriplets.countTriplets(arr, r));
    }

    @Test
    public void testCaseRatio3() {
        List<Long> arr = Arrays.asList(9L, 27L, 81L, 243L, 3L, 9L, 27L);
        long r = 3L;
        assertEquals(6, CountTriplets.countTriplets(arr, r));
    }

    @Test
    public void testCaseNoTriplets() {
        List<Long> arr = Arrays.asList(1L, 2L, 5L, 7L);
        long r = 3L;
        assertEquals(0, CountTriplets.countTriplets(arr, r));
    }
}