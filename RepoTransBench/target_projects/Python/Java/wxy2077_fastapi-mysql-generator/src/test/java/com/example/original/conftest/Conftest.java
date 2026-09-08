package com.example.original.conftest;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class Conftest {

    @Test
    void testTrue() {
        assertTrue(true, "Basic sanity check");
    }

    @Test
    void testNotNull() {
        String x = "abc";
        assertNotNull(x, "x should not be null");
    }
}