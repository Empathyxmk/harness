package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicIpynbWrappersTest {
    // Wrapper to simulate public display for LaTeX in ipython.

    static String wrapMath(String s) {
        return "$" + s + "$";
    }

    @Test
    void testWrapMath() {
        assertEquals("$x+y$", wrapMath("x+y"));
        assertEquals("$a-b$", wrapMath("a-b"));
    }
}