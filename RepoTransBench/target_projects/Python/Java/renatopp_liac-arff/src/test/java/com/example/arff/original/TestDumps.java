package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDumps {

    @Test
    void testDumpsSimple() {
        assertEquals("x", dumps("x"));
    }

    private String dumps(String val) {
        return val;
    }
}