package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestEncodeComment {

    @Test
    void testEncodeComment() {
        String comment = "just a comment";
        assertEquals("% just a comment", encodeComment(comment));
    }

    private String encodeComment(String c) {
        return "%" + " " + c;
    }
}