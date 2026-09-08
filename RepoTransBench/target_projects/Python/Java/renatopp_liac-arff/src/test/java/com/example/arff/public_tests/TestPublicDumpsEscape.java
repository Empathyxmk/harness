package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDumpsEscape {

    @Test
    void testPublicDumpsEscapeQuote() {
        assertEquals("hello\\'world", dumpsEscape("hello'world"));
    }

    private String dumpsEscape(String val) {
        return val.replace("'", "\\'");
    }
}