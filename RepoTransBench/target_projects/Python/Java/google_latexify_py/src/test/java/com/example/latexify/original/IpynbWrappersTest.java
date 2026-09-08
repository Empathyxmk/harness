package com.example.latexify.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IpynbWrappersTest {

    // Simulate a Jupyter display wrapper (returns latex or text display)
    static String wrapLatex(String latex, boolean displayMath) {
        if (displayMath) {
            return "$$" + latex + "$$";
        } else {
            return "$" + latex + "$";
        }
    }

    @Test
    void testWrapLatexDisplayMath() {
        assertEquals("$$\\frac{a}{b}$$", wrapLatex("\\frac{a}{b}", true));
    }

    @Test
    void testWrapLatexInline() {
        assertEquals("$x+y$", wrapLatex("x+y", false));
    }
}