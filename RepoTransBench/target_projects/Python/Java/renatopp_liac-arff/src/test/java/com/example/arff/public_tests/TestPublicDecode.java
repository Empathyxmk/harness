package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecode {

    @Test
    void testPublicDecodeRelation() {
        String input = "@RELATION xyz";
        assertEquals("xyz", getRel(input));
    }

    private String getRel(String line) {
        if (line.toLowerCase().startsWith("@relation")) {
            return line.substring(10).trim();
        }
        return "";
    }
}