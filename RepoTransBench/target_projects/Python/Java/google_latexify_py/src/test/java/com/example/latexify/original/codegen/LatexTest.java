package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class LatexTest {

    static String wrapLatexBlock(String expr) {
        return "$$" + expr + "$$";
    }

    @Test
    void testWrapLatexBlock() {
        assertEquals("$$block$$", wrapLatexBlock("block"));
    }
}