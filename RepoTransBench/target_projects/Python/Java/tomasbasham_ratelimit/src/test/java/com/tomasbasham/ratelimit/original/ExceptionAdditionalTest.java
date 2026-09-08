package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.exception.RateLimitException;

public class ExceptionAdditionalTest {
    @Test
    void testRateLimitExceptionFields() {
        RateLimitException e = new RateLimitException("too many", 3.5);
        assertEquals("too many", e.getMessage());
        assertEquals(3.5, e.getPeriodRemaining(), 1e-9);
    }
}