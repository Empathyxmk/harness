package com.example.latexify.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GenerateLatexTest2 {

    static String latexifyEquation(String left, String right) {
        return "$" + left + "=" + right + "$";
    }

    @Test
    void testLatexifyEquationSimple() {
        assertEquals("$y=x+1$", latexifyEquation("y", "x+1"));
    }

    @Test
    void testLatexifyEquationEmpty() {
        assertEquals("$=$", latexifyEquation("", ""));
    }
}