package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PeriodicTest {
    @Test
    public void testPeriodicExecutionSimulation() {
        int count = 0;
        for (int i = 0; i < 10; i++) {
            count += i;
        }
        assertEquals(45, count);
    }
}