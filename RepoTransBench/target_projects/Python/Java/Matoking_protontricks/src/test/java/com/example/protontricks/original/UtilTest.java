package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class UtilTest {
    static Map<String, Object> lowerDict(Map<String, ?> d) {
        Map<String, Object> lowered = new HashMap<>();
        for (Map.Entry<String, ?> e : d.entrySet()) {
            String k = e.getKey().toLowerCase();
            Object v = e.getValue();
            if (v instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, ?> vMap = (Map<String, ?>) v;
                lowered.put(k, lowerDict(vMap));
            } else {
                lowered.put(k, v);
            }
        }
        return lowered;
    }

    @Test
    void testLowerDict_oneLevel() {
        Map<String, Object> input = Map.of("KEY", 1, "AnOtHeR", 2);
        Map<String, Object> result = lowerDict(input);
        assertTrue(result.containsKey("key"));
        assertTrue(result.containsKey("another"));
        assertFalse(result.containsKey("KEY"));
        assertFalse(result.containsKey("AnOtHeR"));
    }

    @Test
    void testLowerDict_nested() {
        Map<String, Object> nested = new HashMap<>();
        nested.put("X", 10);
        Map<String, Object> input = new HashMap<>();
        input.put("A", 1);
        input.put("NESTED", nested);
        input.put("B", "str");
        Map<String, Object> result = lowerDict(input);
        assertTrue(result.containsKey("nested"));
        assertTrue(((Map)result.get("nested")).containsKey("x"));
    }
}