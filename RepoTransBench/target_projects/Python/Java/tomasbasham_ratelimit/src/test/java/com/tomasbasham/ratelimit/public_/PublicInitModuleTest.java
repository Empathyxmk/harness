package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.tomasbasham.ratelimit.*;

public class PublicInitModuleTest {

    @Test
    void testPublicInitModuleAllExports() {
        java.util.Set<String> exported = new java.util.HashSet<>();
        for (String name : Ratelimit.__all__)
            exported.add(name);
        for (String name : exported) {
            assertNotNull(Ratelimit.getattr(name), "Missing public API: " + name);
        }
    }

    @Test
    void testPublicInitLimitsAndRateLimitedAreDecorator() {
        assertEquals(Ratelimit.limits.toString(), Ratelimit.RateLimitDecorator.toString());
        assertEquals(Ratelimit.rate_limited.toString(), Ratelimit.RateLimitDecorator.toString());
        assertNotNull(Ratelimit.limits);
        assertNotNull(Ratelimit.rate_limited);
    }

    @Test
    void testPublicVersionStringLength() {
        String v = Ratelimit.__version__;
        assertTrue(v instanceof String);
        assertTrue(v.chars().filter(ch -> ch == '.').count() >= 2, "Should have at least two dots");
    }
}