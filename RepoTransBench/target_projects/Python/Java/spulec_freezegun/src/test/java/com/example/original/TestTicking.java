package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestTicking {

    @Test
    public void testTickingTime() throws InterruptedException {
        long before = System.currentTimeMillis();
        Thread.sleep(10);
        long after = System.currentTimeMillis();
        assertTrue(after >= before, "Time did not tick forward as expected.");
    }
}