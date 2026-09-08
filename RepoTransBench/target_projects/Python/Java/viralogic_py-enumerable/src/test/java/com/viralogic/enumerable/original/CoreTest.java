package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;

class CoreTest {

    @Test
    void testBasicEnumerableIteration() {
        List<Integer> data = Arrays.asList(1, 2, 3);
        List<Integer> output = new ArrayList<>();
        for (Integer i : data) {
            output.add(i);
        }
        assertEquals(Arrays.asList(1, 2, 3), output);
    }

    @Test
    void testMapSelect() {
        List<String> data = Arrays.asList("a", "b", "c");
        List<String> upper = new ArrayList<>();
        for (String s : data) {
            upper.add(s.toUpperCase());
        }
        assertEquals(Arrays.asList("A", "B", "C"), upper);
    }

    @Test
    void testFilterWhere() {
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> evens = new ArrayList<>();
        for (Integer i : data) {
            if (i % 2 == 0) {
                evens.add(i);
            }
        }
        assertEquals(Arrays.asList(2, 4), evens);
    }

    @Test
    void testZip() {
        List<Integer> a = Arrays.asList(1, 2, 3);
        List<String> b = Arrays.asList("a", "b", "c");
        List<String> zipped = new ArrayList<>();
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
            zipped.add(a.get(i) + b.get(i));
        }
        assertEquals(Arrays.asList("1a", "2b", "3c"), zipped);
    }

    @Test
    void testSum() {
        List<Integer> data = Arrays.asList(1, 2, 3, 4);
        int sum = 0;
        for (Integer i : data)
            sum += i;
        assertEquals(10, sum);
    }
}