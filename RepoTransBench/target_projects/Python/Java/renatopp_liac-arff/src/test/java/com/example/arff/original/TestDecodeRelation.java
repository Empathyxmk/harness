package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDecodeRelation {

    @Test
    void testDecodeRel() {
        String line = "@RELATION newrel";
        assertEquals("newrel", decodeRelation(line));
    }

    private String decodeRelation(String line) {
        if (line.toLowerCase().startsWith("@relation")) {
            return line.substring(10).trim();
        }
        return "";
    }
}