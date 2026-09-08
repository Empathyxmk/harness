package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.exception.RateLimitException;

public class ExceptionTest {
    @Test
    void testRateLimitExceptionMessageAndPeriod() {
        RateLimitException e = new RateLimitException("limit reached", 4.5);
        assertTrue(e instanceof RateLimitException);
        assertEquals(4.5, e.getPeriodRemaining(), 1e-9);
        assertEquals("limit reached", e.getMessage());
    }
}