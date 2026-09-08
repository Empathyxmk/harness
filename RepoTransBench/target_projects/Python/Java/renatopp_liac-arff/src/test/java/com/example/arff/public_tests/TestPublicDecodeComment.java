package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecodeComment {

    @Test
    void testPublicDecodeComment() {
        String comment = "% random comment";
        assertEquals("random comment", decodeComment(comment));
    }

    private String decodeComment(String line) {
        return line.startsWith("%") ? line.substring(1).trim() : "";
    }
}