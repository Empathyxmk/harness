package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.exception.RateLimitException;

public class PublicExceptionAdditionalTest {
    @Test
    void testPublicRateLimitExceptionFields() {
        RateLimitException e = new RateLimitException("limit reached", 1.25);
        assertEquals("limit reached", e.getMessage());
        assertEquals(1.25, e.getPeriodRemaining(), 1e-9);
    }
}