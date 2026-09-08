package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicConversor {

    @Test
    void testPublicConversorDummy() {
        // Dummy conversor test: convert int to string
        int value = 10;
        assertEquals("10", Integer.toString(value));
    }
}