package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;
import com.tomasbasham.ratelimit.decorators.SleepAndRetry;
import com.tomasbasham.ratelimit.exception.RateLimitException;

public class PublicDecoratorsEdgeCasesTest {

    @Test
    void testPublicNegativePeriod() {
        RateLimitDecorator d = new RateLimitDecorator(1, -2);
        java.util.List<Integer> callcount = new java.util.ArrayList<>();
        java.util.function.Supplier<Integer> f = d.decorate(() -> {
            callcount.add(1);
            return 7;
        });
        assertEquals(7, (int)f.get());
        assertThrows(RateLimitException.class, f::get);
    }

    @Test
    void testPublicSleepAndRetrySucceeds() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(1, 0.02);
        java.util.List<Long> callTimes = new java.util.ArrayList<>();
        SleepAndRetry sar = new SleepAndRetry();
        java.util.function.Supplier<Integer> fun = sar.decorate(rl.decorate(() -> {
            callTimes.add(System.currentTimeMillis());
            return 17;
        }));
        assertEquals(17, (int)fun.get());
        long t0 = System.currentTimeMillis();
        int res = fun.get();
        assertEquals(17, res);
        assertTrue(System.currentTimeMillis() - t0 >= 20, "Should sleep at least 20ms");
    }

    @Test
    void testPublicSleepAndRetryMultiple() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(2, 0.015);
        final int[] counter = {0};
        SleepAndRetry sar = new SleepAndRetry();
        java.util.function.Supplier<Integer> g = sar.decorate(rl.decorate(() -> {
            counter[0] += 2;
            return counter[0];
        }));
        assertEquals(2, (int)g.get());
        assertEquals(4, (int)g.get());
        long t0 = System.currentTimeMillis();
        int val = g.get();
        assertEquals(6, val);
        assertEquals(6, counter[0]);
        assertTrue(System.currentTimeMillis() - t0 >= 15, "Should sleep at least 15ms");
    }
}