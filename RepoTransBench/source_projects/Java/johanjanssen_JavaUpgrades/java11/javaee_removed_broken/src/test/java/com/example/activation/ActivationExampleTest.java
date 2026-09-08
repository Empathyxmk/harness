package com.example.activation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ActivationExampleTest {

    @Test
    public void testMainNoExceptions() {
        // Just ensure main runs without throwing
        assertDoesNotThrow(() -> ActivationExample.main(new String[0]));
    }
}