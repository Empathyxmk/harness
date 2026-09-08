package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicUtilTest {

    @Test
    public void testPublicFlattenDict() {
        Map<String, Object> m = new HashMap<>();
        m.put("a", 1);
        Map<String, Object> result = flattenDict(m);
        assertEquals(1, result.size());
        assertEquals(1, result.get("a"));
    }

    // Simple flatten which just unwraps top-level
    public static Map<String, Object> flattenDict(Map<String, Object> dic) {
        Map<String, Object> flat = new HashMap<>();
        for (Map.Entry<String, Object> e : dic.entrySet()) {
            flat.put(e.getKey(), e.getValue());
        }
        return flat;
    }
}