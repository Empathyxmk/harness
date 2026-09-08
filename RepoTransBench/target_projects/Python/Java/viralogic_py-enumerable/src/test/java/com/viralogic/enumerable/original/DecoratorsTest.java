package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class DecoratorsTest {

    @Test
    void testOrderByAscending() {
        List<String> items = Arrays.asList("cat", "dog", "ant", "bee");
        List<String> sorted = new ArrayList<>(items);
        sorted.sort(Comparator.naturalOrder());
        assertEquals(Arrays.asList("ant", "bee", "cat", "dog"), sorted);
    }

    @Test
    void testOrderByDescending() {
        List<Integer> items = Arrays.asList(4, 2, 5, 1, 3);
        List<Integer> sorted = new ArrayList<>(items);
        sorted.sort(Comparator.reverseOrder());
        assertEquals(Arrays.asList(5, 4, 3, 2, 1), sorted);
    }

    @Test
    void testGroupBy() {
        List<String> animals = Arrays.asList("cat", "dog", "ant", "bat");
        Map<Character, List<String>> grouped = new HashMap<>();
        for (String s : animals) {
            grouped.computeIfAbsent(s.charAt(0), k -> new ArrayList<>()).add(s);
        }
        assertEquals(Arrays.asList("ant"), grouped.get('a'));
        assertEquals(Arrays.asList("bat"), grouped.get('b'));
        assertEquals(Arrays.asList("cat'), grouped.get('c'));
        assertEquals(Arrays.asList("dog"), grouped.get('d'));
    }
}