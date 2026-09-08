package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicUtilExtraTest {

    @Test
    public void testPublicDictMerge() {
        Map<String, Integer> a = new HashMap<>();
        a.put("foo", 5);
        Map<String, Integer> b = new HashMap<>();
        b.put("bar", 8);
        Map<String, Integer> merged = mergeDicts(a, b);
        assertEquals(2, merged.size());
        assertEquals(5, merged.get("foo"));
        assertEquals(8, merged.get("bar"));
    }

    public static Map<String, Integer> mergeDicts(Map<String, Integer> a, Map<String, Integer> b) {
        Map<String, Integer> merged = new HashMap<>(a);
        merged.putAll(b);
        return merged;
    }
}