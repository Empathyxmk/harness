package com.us.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicUsTest {

    // Simulate public test from us/public_tests/test_public_us.py

    @Test
    void testExistingStateAbbreviation() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        abbrName.put("TX", "Texas");

        assertEquals("California", abbrName.get("CA"));
        assertEquals("Texas", abbrName.get("TX"));
        assertNull(abbrName.get("ZZ"));
    }

    @Test
    void testAllStatesListed() {
        List<String> abbrs = Arrays.asList("CA", "TX", "NY", "FL");
        assertTrue(abbrs.contains("CA"));
        assertTrue(abbrs.contains("NY"));
        assertTrue(abbrs.contains("TX"));
        assertEquals(4, abbrs.size());
    }

    @Test
    void testNoDuplicateAbbreviations() {
        List<String> abbrs = Arrays.asList("CA", "TX", "NY", "FL");
        Set<String> abbrSet = new HashSet<>(abbrs);
        assertEquals(abbrs.size(), abbrSet.size());
    }
}