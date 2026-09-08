package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AssignmentReducerTest {

    static String reduceAssignment(String code) {
        // converts "x = x + 1" to "x += 1"
        return code.replaceAll("(\\w+) = \\1 \\+ (\\d+)", "$1 += $2");
    }

    @Test
    void testReduceAssignment() {
        assertEquals("x += 1", reduceAssignment("x = x + 1"));
        assertEquals("y = z + 1", reduceAssignment("y = z + 1")); // no reduction
    }
}