package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDecodeAttributeTypes {

    @Test
    void testDecodeAttributeTypeNumeric() {
        String attributeLine = "@ATTRIBUTE age NUMERIC";
        assertEquals("age", getName(attributeLine));
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