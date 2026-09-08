package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.Collectors;

class FunctionsTest {

    @Test
    void testConcat() {
        List<Integer> a = Arrays.asList(1, 2);
        List<Integer> b = Arrays.asList(3, 4);
        List<Integer> c = new ArrayList<>(a);
        c.addAll(b);
        assertEquals(Arrays.asList(1, 2, 3, 4), c);
    }

    @Test
    void testDistinct() {
        List<Integer> vals = Arrays.asList(1, 2, 2, 3, 1, 4);
        List<Integer> distinct = vals.stream().distinct().collect(Collectors.toList());
        assertEquals(Arrays.asList(1, 2, 3, 4), distinct);
    }

    @Test
    void testContains() {
        List<String> vals = Arrays.asList("a", "b", "c");
        assertTrue(vals.contains("b"));
        assertFalse(vals.contains("x"));
    }

    @Test
    void testAppendAndPrepend() {
        List<Integer> data = new ArrayList<>(Arrays.asList(2, 3, 4));
        data.add(0, 1);       // prepend
        data.add(5);          // append
        assertEquals(Arrays.asList(1, 2, 3, 4, 5), data);
    }

    @Test
    void testReverse() {
        List<Integer> data = Arrays.asList(1,2,3,4,5);
        List<Integer> reversed = new ArrayList<>(data);
        Collections.reverse(reversed);
        assertEquals(Arrays.asList(5,4,3,2,1), reversed);
    }
}