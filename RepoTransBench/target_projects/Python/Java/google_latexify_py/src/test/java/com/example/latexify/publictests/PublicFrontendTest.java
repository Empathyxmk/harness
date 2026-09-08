package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicFrontendTest {
    // Simulate public facing frontend helpers for LaTeX rendering

    static String renderLatex(String s) {
        return "$" + s + "$";
    }

    @Test
    void testPublicRenderLatex() {
        assertEquals("$f(x)$", renderLatex("f(x)"));
        assertEquals("$a+b$", renderLatex("a+b"));
    }
}