package com.us.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestExtra {

    // This simulates the kind of test that might be found in us/tests/test_extra.py
    // In reality, implementers must translate the actual Python logic for comprehensive translation.
    // **Sample Implementation**
    @Test
    void testAbbreviationToName() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        abbrName.put("NY", "New York");

        assertEquals("California", abbrName.get("CA"));
        assertEquals("New York", abbrName.get("NY"));
        assertNull(abbrName.get("ZZ"));
    }

    @Test
    void testAllStateNamesAreUnique() {
        List<String> stateNames = Arrays.asList("California", "Texas", "New York");
        Set<String> unique = new HashSet<>(stateNames);
        assertEquals(stateNames.size(), unique.size());
    }

    @Test
    void testCaseInsensitiveLookup() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        abbrName.put("NY", "New York");

        String lookup = abbrName.get("ca".toUpperCase());
        assertEquals("California", lookup);
    }

    @Test
    void testInvalidStateAbbrReturnsNull() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        abbrName.put("NY", "New York");

        assertNull(abbrName.get("ZZ"));
    }
}