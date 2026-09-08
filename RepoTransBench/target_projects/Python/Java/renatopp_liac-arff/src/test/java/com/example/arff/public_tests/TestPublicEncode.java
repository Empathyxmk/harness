package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicEncode {

    @Test
    void testPublicEncodeStr() {
        assertEquals("'foo'", encode("foo"));
    }

    @Test
    void testPublicEncodeApostrophe() {
        assertEquals("'a\\'b'", encode("a'b"));
    }

    private String encode(String val) {
        return "'" + val.replace("'", "\\'") + "'";
    }
}