package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicErrors {

    @Test
    public void testErrorThrown() {
        Exception e = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("Some Error");
        });
        assertEquals("Some Error", e.getMessage());
    }
}