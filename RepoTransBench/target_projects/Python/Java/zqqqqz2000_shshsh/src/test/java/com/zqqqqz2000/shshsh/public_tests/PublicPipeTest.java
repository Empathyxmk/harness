package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicPipeTest {

    List<Integer> doubleNumbers(List<Integer> nums) {
        List<Integer> res = new ArrayList<>();
        for (Integer i : nums) res.add(i * 2);
        return res;
    }

    List<Integer> filterEven(List<Integer> nums) {
        List<Integer> res = new ArrayList<>();
        for (Integer i : nums) if (i % 2 == 0) res.add(i);
        return res;
    }

    @Test
    void testPipeDoubleThenFilterEven() {
        List<Integer> in = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> doubled = doubleNumbers(in);
        List<Integer> evens = filterEven(doubled);
        assertIterableEquals(Arrays.asList(2, 4, 6, 8, 10), doubled);
        assertIterableEquals(Arrays.asList(2, 4, 6, 8, 10), evens);
    }

    @Test
    void testPipeOriginalOrder() {
        List<Integer> in = Arrays.asList(1, 3, 5);
        List<Integer> doubled = doubleNumbers(in);
        assertIterableEquals(Arrays.asList(2, 6, 10), Arrays.asList(2, 6, 10));
    }
}