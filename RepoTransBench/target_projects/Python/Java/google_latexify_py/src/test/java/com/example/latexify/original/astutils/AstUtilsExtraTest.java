package com.example.latexify.original.astutils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AstUtilsExtraTest {

    static int countOperators(String expr) {
        int count = 0;
        for (char c : expr.toCharArray()) {
            if ("+-*/^".indexOf(c) >= 0) count++;
        }
        return count;
    }

    @Test
    void testCountOperators() {
        assertEquals(3, countOperators("a+b-c*d"));
        assertEquals(0, countOperators("foo"));
    }
}