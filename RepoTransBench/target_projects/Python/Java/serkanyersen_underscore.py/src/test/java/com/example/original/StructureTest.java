package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class StructureTest {
    @Test
    void testPairs() {
        Map<String, Integer> map = new HashMap<>();
        map.put("a", 1);
        map.put("b", 2);
        List<Map.Entry<String, Integer>> pairs = Underscore.pairs(map);
        // Can't guarantee order, but all must be present
        Set<Map.Entry<String, Integer>> expected = new HashSet<>();
        expected.add(new AbstractMap.SimpleEntry<>("a", 1));
        expected.add(new AbstractMap.SimpleEntry<>("b", 2));
        assertEquals(expected, new HashSet<>(pairs));
    }
}