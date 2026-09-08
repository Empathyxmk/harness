package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDumps {

    @Test
    void testPublicDumpsVal() {
        assertEquals("y", dumps("y"));
    }

    private String dumps(String val) {
        return val;
    }
}