package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicStructureTest {
    @Test
    void testPairsPublic() {
        Map<String, Integer> map = new HashMap<>();
        map.put("foo", 7);
        map.put("bar", 8);
        List<Map.Entry<String, Integer>> pairs = Underscore.pairs(map);
        Set<Map.Entry<String, Integer>> expected = new HashSet<>();
        expected.add(new AbstractMap.SimpleEntry<>("foo", 7));
        expected.add(new AbstractMap.SimpleEntry<>("bar", 8));
        assertEquals(expected, new HashSet<>(pairs));
    }
}