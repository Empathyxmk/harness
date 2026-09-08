package com.example.latexify.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GenerateLatexTest {

    // Dummy simulate generation - true implementation would parse AST to latex
    static String generateLatex(String expr) {
        // For demo: just add "$$" or "$" around some expressions to simulate block/inline mode.
        if (expr == null) return null;
        if (expr.startsWith("def")) {
            return "$$" + expr.replace("def ", "").replace(":", "") + "$$";
        }
        return "$" + expr + "$";
    }

    @Test
    void testGenerateLatexSimpleExpressionBlock() {
        assertEquals("$$f(x)=x^2+1$$", generateLatex("def f(x): x^2+1"));
    }

    @Test
    void testGenerateLatexSimpleExpressionInline() {
        assertEquals("$a+b$", generateLatex("a+b"));
    }

    @Test
    void testGenerateLatexNull() {
        assertNull(generateLatex(null));
    }
}