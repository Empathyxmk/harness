package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestEncode {

    @Test
    void testEncodeString() {
        assertEquals("'hello'", encode("hello"));
    }

    @Test
    void testEncodeWithApostrophe() {
        assertEquals("'it\\'s'", encode("it's"));
    }

    private String encode(String s) {
        return "'" + s.replace("'", "\\'") + "'";
    }
}