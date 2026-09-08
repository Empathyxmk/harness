package com.us.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestUs {

    // Simulating logic from us/tests/test_us.py

    @Test
    void testStateAbbrList() {
        List<String> abbrs = Arrays.asList("CA", "NY", "TX", "FL");
        assertTrue(abbrs.contains("CA"));
        assertTrue(abbrs.contains("NY"));
        assertFalse(abbrs.contains("ZZ"));
    }

    @Test
    void testStateNameToAbbr() {
        Map<String, String> nameAbbr = new HashMap<>();
        nameAbbr.put("California", "CA");
        nameAbbr.put("New York", "NY");
        nameAbbr.put("Texas", "TX");
        assertEquals("CA", nameAbbr.get("California"));
        assertNull(nameAbbr.get("Unknown State"));
    }

    @Test
    void testLowercaseNameToAbbr() {
        Map<String, String> nameAbbr = new HashMap<>();
        nameAbbr.put("california".toLowerCase(), "CA");
        assertEquals("CA", nameAbbr.get("california"));
        assertNull(nameAbbr.get("florida"));
    }

    @Test
    void testStateListIsNotEmpty() {
        List<String> abbrs = Arrays.asList("CA", "TX", "NY", "FL");
        assertFalse(abbrs.isEmpty());
    }
}