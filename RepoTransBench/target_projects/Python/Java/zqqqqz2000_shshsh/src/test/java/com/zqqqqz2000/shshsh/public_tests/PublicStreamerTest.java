package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.stream.*;

class PublicStreamerTest {
    List<Integer> ints = Arrays.asList(1, 2, 3, 4, 5);
    List<String> strs = Arrays.asList("a", "bb", "ccc");

    @Test
    void testStreamSum() {
        int sum = ints.stream().mapToInt(Integer::intValue).sum();
        assertEquals(15, sum);
    }

    @Test
    void testStreamMap() {
        List<Integer> lens = strs.stream().map(String::length).collect(Collectors.toList());
        assertIterableEquals(Arrays.asList(1, 2, 3), lens);
    }
}