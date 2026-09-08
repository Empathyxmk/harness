package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecodeRelation {

    @Test
    void testPublicDecodeRelationValue() {
        String line = "@RELATION abc";
        assertEquals("abc", decodeRelation(line));
    }

    private String decodeRelation(String line) {
        if (line.toLowerCase().startsWith("@relation")) {
            return line.substring(10).trim();
        }
        return "";
    }
}