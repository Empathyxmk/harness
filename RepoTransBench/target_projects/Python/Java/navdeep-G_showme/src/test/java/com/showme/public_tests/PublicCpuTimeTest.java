package com.showme.public_tests;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicCpuTimeTest {
    @Test
    void testPublicCputimeRuns() {
        double value = Core.cputime();
        assertTrue(value >= 0);
        // No upper bound: just ensure non-negative float
    }
}