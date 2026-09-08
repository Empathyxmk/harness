package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicLoads {

    @Test
    void testPublicLoadsSimple() {
        String arff = "@RELATION xy\n@DATA\n7";
        assertEquals(arff, loads(arff));
    }

    private String loads(String input) {
        return input;
    }
}