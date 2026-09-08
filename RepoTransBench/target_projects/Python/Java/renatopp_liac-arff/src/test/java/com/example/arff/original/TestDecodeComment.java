package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDecodeComment {

    @Test
    void testDecodeCommentLine() {
        String line = "% a comment";
        assertEquals("a comment", decodeComment(line));
    }

    private String decodeComment(String line) {
        return line.startsWith("%") ? line.substring(1).trim() : "";
    }
}