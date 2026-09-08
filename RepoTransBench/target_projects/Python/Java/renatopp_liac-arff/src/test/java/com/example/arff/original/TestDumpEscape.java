package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDumpEscape {

    @Test
    void testEscapeQuote() {
        assertEquals("a\\'b", escape("a'b"));
    }

    private String escape(String val) {
        return val.replace("'", "\\'");
    }
}