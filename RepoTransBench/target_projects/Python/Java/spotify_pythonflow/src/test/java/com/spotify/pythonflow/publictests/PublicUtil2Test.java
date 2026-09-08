package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicUtil2Test {

    @Test
    public void testPublicFlattenDictEmpty() {
        Map<String, Object> m = new HashMap<>();
        Map<String, Object> result = PublicUtilTest.flattenDict(m);
        assertTrue(result.isEmpty());
    }
}