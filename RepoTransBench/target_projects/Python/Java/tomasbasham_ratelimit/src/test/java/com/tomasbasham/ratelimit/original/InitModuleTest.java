package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.*;

public class InitModuleTest {

    @Test
    void testInitModuleAllExports() {
        // Assume Ratelimit.__all__ gives list of public attributes
        for (String name : Ratelimit.__all__) {
            assertTrue(Ratelimit.hasattr(name),
                "Ratelimit should have attribute '" + name + "'");
        }
    }

    @Test
    void testInitLimitsAndRateLimitedAreDecorator() {
        assertSame(Ratelimit.limits, Ratelimit.RateLimitDecorator, "limits should be RateLimitDecorator class");
        assertSame(Ratelimit.rate_limited, Ratelimit.RateLimitDecorator, "rate_limited should be RateLimitDecorator class");
        assertTrue(Ratelimit.limits instanceof java.util.function.Function || Ratelimit.limits instanceof java.util.function.Supplier || Ratelimit.limits != null);
        assertTrue(Ratelimit.rate_limited instanceof java.util.function.Function || Ratelimit.rate_limited instanceof java.util.function.Supplier || Ratelimit.rate_limited != null);
    }

    @Test
    void testVersionStringExists() {
        String v = Ratelimit.__version__;
        assertNotNull(v);
        assertTrue(v instanceof String, "Version is not a string");
        assertTrue(v.contains("."));
    }
}