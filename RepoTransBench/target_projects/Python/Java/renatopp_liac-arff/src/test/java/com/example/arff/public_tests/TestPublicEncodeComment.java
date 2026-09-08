package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicEncodeComment {

    @Test
    void testPublicEncodeComment() {
        String comment = "foobar";
        assertEquals("% foobar", encodeComment(comment));
    }

    private String encodeComment(String c) {
        return "%" + " " + c;
    }
}