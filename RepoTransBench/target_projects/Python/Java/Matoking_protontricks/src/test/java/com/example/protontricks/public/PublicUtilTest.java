package com.example.protontricks.public;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class PublicUtilTest {
    /**
     * Simulates util.lower_dict - recursively lowercases all string keys
     */
    public static Map<String, Object> lowerDict(Map<String, ?> d) {
        Map<String, Object> lowered = new HashMap<>();
        for (Map.Entry<String, ?> e : d.entrySet()) {
            String k = e.getKey().toLowerCase();
            Object v = e.getValue();
            if (v instanceof Map<?, ?>) {
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
    void testPublicLowerDict() {
        Map<String, Object> upperDict = new HashMap<>();
        upperDict.put("KEY", 10);
        upperDict.put("ALPHA", 20);
        upperDict.put("Z", "VALUE");
        upperDict.put("MiXeD", "Flag");
        upperDict.put("foo", "Bar");
        Map<String, Object> lowered = lowerDict(upperDict);

        Map<String, Object> expected = new HashMap<>();
        expected.put("key", 10);
        expected.put("alpha", 20);
        expected.put("z", "VALUE");
        expected.put("mixed", "Flag");
        expected.put("foo", "Bar");

        assertEquals(expected, lowered);
    }
}