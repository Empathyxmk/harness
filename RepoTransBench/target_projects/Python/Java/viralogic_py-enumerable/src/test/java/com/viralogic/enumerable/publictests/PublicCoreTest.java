package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.*;

class PublicCoreTest {

    @Test
    void testSumPublic() {
        List<Integer> a = Arrays.asList(2,3,4);
        int sum = a.stream().mapToInt(Integer::intValue).sum();
        assertEquals(9, sum);
    }

    @Test
    void testMapSelectPublic() {
        List<String> a = Arrays.asList("hello", "world");
        List<Integer> lens = a.stream().map(String::length).collect(Collectors.toList());
        assertEquals(Arrays.asList(5, 5), lens);
    }
}