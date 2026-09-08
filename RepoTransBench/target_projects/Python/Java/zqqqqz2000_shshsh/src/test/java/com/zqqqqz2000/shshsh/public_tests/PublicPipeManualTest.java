package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicPipeManualTest {
    static List<Integer> add1(List<Integer> nums) {
        List<Integer> res = new ArrayList<>();
        for (int n : nums) res.add(n + 1);
        return res;
    }

    static List<Integer> mul2(List<Integer> nums) {
        List<Integer> res = new ArrayList<>();
        for (int n : nums) res.add(n * 2);
        return res;
    }

    @Test
    void testPipeManual() {
        List<Integer> result = mul2(add1(Arrays.asList(1, 2, 3)));
        assertIterableEquals(Arrays.asList(4, 6, 8), result);
    }

    @Test
    void testPipeManualWithEmpty() {
        List<Integer> empty = Collections.emptyList();
        List<Integer> result = mul2(add1(empty));
        assertTrue(result.isEmpty());
    }
}