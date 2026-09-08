package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FunctionExpanderTest {

    static String expandF(String fCall) {
        // For demo, expands "f(a)" to "a+1"
        if (fCall.startsWith("f(")) return "a+1";
        return fCall;
    }

    @Test
    void testExpandF() {
        assertEquals("a+1", expandF("f(a)"));
        assertEquals("b", expandF("b"));
    }
}