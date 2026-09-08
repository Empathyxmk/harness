package com.example.transaction;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TransactionExamplePublicTest {
    @Test
    void testTransactionalWorkPublic() {
        TransactionExample tx = new TransactionExample();
        assertTrue(tx.doTransaction().length() > 0, "Returned string should not be empty");
    }
}