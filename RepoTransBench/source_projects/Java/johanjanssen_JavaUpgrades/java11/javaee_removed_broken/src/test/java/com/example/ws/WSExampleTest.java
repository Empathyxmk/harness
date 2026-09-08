package com.example.ws;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class WSExampleTest {
    @Test
    public void testMainNoExceptions() {
        assertDoesNotThrow(() -> WSExample.main(new String[0]));
    }
}