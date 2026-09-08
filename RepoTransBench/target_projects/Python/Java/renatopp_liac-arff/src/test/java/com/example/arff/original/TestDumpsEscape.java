package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDumpsEscape {

    @Test
    void testDumpsEscapeQuote() {
        assertEquals("foo\\'bar", dumpsEscape("foo'bar"));
    }

    private String dumpsEscape(String val) {
        return val.replace("'", "\\'");
    }
}