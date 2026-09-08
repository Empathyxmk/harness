package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.tomasbasham.ratelimit.exception.RateLimitException;

public class PublicExceptionTest {

    @Test
    void testPublicRateLimitExceptionInheritance() {
        RateLimitException ex = new RateLimitException("foo", 0.99);
        assertTrue(ex instanceof Exception);
        assertTrue(Double.isFinite(ex.getPeriodRemaining()));
    }

    @Test
    void testPublicExceptionStrAndValue() {
        RateLimitException ex = new RateLimitException("overload", 2.0);
        assertEquals("overload", ex.getMessage());
        assertEquals(2.0, ex.getPeriodRemaining(), 1e-9);
    }
}