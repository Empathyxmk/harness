package com.example.transaction;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TransactionExampleTest {
    @Test
    public void testMainNoExceptions() {
        assertDoesNotThrow(() -> TransactionExample.main(new String[0]));
    }
}