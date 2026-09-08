package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.util.HashMap;
import java.util.TreeMap;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultMappingTest {

    @Test
    void testMappingBasic() {
        HashMap<String, Double> mapping = new HashMap<>();
        mapping.put("pi", 3.1415);
        mapping.put("e", 2.7183);
        assertTrue(mapping.containsKey("pi"));
        assertEquals(2.7183, mapping.get("e"), 1e-8);
    }

    @Test
    void testMappingSorted() {
        TreeMap<String, Integer> sorted = new TreeMap<>();
        sorted.put("baz", 1);
        sorted.put("foo", 3);
        sorted.put("bar", 2);
        assertEquals("[bar, baz, foo]", sorted.keySet().toString());
    }
}