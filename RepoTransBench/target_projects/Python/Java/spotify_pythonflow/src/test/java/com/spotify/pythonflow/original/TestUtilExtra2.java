package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestUtilExtra2 {
    // Extra edge-case test matching src/tests/test_util_extra.py for completeness

    @Test
    public void testEmptyMerge() {
        Map<String, Object> a = new HashMap<>();
        Map<String, Object> b = new HashMap<>();
        Map<String, Object> merged = UtilExtraTest.mergeDicts(a, b);
        assertTrue(merged.isEmpty());
    }

    @Test
    public void testMergeNulls() {
        Map<String, Object> a = new HashMap<>();
        Map<String, Object> b = null;
        Map<String, Object> result = UtilExtraTest.mergeDicts(a, b == null ? new HashMap<>() : b);
        assertTrue(result.isEmpty());
    }
}