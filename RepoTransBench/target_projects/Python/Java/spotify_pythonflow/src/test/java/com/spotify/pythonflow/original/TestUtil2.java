package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestUtil2 {
    // Extra edge-case test matching src/tests/test_util.py for completeness

    @Test
    public void testFlattenDictEmpty() {
        Map<String, Object> dic = new HashMap<>();
        Map<String, Object> flat = UtilTest.flattenDict(dic);
        assertTrue(flat.isEmpty());
    }

    @Test
    public void testFlattenDictNullVals() {
        Map<String, Object> dic = new HashMap<>();
        dic.put("a", null);
        Map<String, Object> flat = UtilTest.flattenDict(dic);
        assertEquals(1, flat.size());
        assertNull(flat.get("a"));
    }
}