package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDecode {

    @Test
    void testDecodeRelation() {
        String input = "@RELATION dataset";
        assertEquals("dataset", getRelationName(input));
    }

    private String getRelationName(String line) {
        if (line.toLowerCase().startsWith("@relation")) {
            return line.substring(10).trim();
        }
        return "";
    }
}