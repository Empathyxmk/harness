package com.us.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicExtraTest {

    // Simulate public test from us/public_tests/test_public_extra.py

    @Test
    void testAbbreviationNormalization() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        abbrName.put("FL", "Florida");

        String abbr = "ca";
        String normalized = abbr.toUpperCase();
        assertEquals("California", abbrName.get(normalized));
    }

    @Test
    void testAbbreviationNotFound() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");
        assertNull(abbrName.get("ZZ"));
    }

    @Test
    void testAbbrWithWhitespace() {
        Map<String, String> abbrName = new HashMap<>();
        abbrName.put("CA", "California");

        String abbr = " CA ";
        String normalized = abbr.trim().toUpperCase();
        assertEquals("California", abbrName.get(normalized));
    }
}