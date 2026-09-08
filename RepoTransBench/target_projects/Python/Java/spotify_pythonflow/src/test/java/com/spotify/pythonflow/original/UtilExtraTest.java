package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class UtilExtraTest {

    @Test
    public void testMergeDict() {
        Map<String, Object> a = new HashMap<>();
        a.put("foo", 1);
        Map<String, Object> b = new HashMap<>();
        b.put("bar", 2);
        Map<String, Object> merged = mergeDicts(a, b);
        assertEquals(2, merged.size());
        assertEquals(1, merged.get("foo"));
        assertEquals(2, merged.get("bar"));
    }

    @Test
    public void testMergeDictOverrides() {
        Map<String, Object> a = new HashMap<>();
        a.put("foo", 1);
        a.put("bar", 2);
        Map<String, Object> b = new HashMap<>();
        b.put("bar", 99); // override
        Map<String, Object> merged = mergeDicts(a, b);
        assertEquals(2, merged.size());
        assertEquals(1, merged.get("foo"));
        assertEquals(99, merged.get("bar"));
    }

    public static Map<String, Object> mergeDicts(Map<String, Object> a, Map<String, Object> b) {
        Map<String, Object> merged = new HashMap<>(a);
        merged.putAll(b);
        return merged;
    }
}