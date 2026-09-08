package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDumpEscape {

    @Test
    void testPublicDumpEscapeQuote() {
        assertEquals("foobar\\'baz", dumpEscape("foobar'baz"));
    }

    private String dumpEscape(String val) {
        return val.replace("'", "\\'");
    }
}