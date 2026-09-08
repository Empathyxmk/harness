package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestErrors {

    @Test
    public void testRaiseError() {
        Exception exception = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("Expected error");
        });
        assertEquals("Expected error", exception.getMessage());
    }
}