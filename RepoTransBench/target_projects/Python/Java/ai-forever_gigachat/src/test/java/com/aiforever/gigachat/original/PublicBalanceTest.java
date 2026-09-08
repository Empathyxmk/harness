package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Balance {
    double amount;

    public Balance(double amount) {
        this.amount = amount;
    }
}

public class PublicBalanceTest {
    @Test
    void testBalanceInit() {
        Balance b = new Balance(123.45);
        assertEquals(123.45, b.amount, 1e-10);
    }

    @Test
    void testBalanceNegative() {
        Balance b = new Balance(-50.0);
        assertTrue(b.amount < 0);
    }
}