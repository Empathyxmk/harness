package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecodeAttributeTypes {

    @Test
    void testPublicDecodeAttributeType() {
        String attributeLine = "@ATTRIBUTE foo NUMERIC";
        assertEquals("foo", getName(attributeLine));
        assertEquals("NUMERIC", getType(attributeLine));
    }

    private String getName(String line) {
        String[] parts = line.split(" ");
        return parts[1];
    }
    private String getType(String line) {
        String[] parts = line.split(" ");
        return parts[2];
    }
}