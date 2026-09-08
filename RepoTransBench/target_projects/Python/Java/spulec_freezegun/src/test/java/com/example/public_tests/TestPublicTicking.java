package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicTicking {

    @Test
    public void testTickingOperation() throws InterruptedException {
        long before = System.currentTimeMillis();
        Thread.sleep(1);
        long after = System.currentTimeMillis();
        assertTrue(after >= before);
    }
}