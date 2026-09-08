package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicOperations {

    @Test
    public void testSum() {
        int value = 42 + 1;
        assertEquals(43, value);
    }
}