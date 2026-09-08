package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicUtilExtra2Test {

    @Test
    public void testPublicDictMergeEmpty() {
        Map<String, Integer> a = new HashMap<>();
        Map<String, Integer> b = new HashMap<>();
        Map<String, Integer> merged = PublicUtilExtraTest.mergeDicts(a, b);
        assertTrue(merged.isEmpty());
    }
}