package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;
import com.tomasbasham.ratelimit.decorators.SleepAndRetry;
import com.tomasbasham.ratelimit.exception.RateLimitException;

public class PublicDecoratorTest {

    @Test
    void testPublicSimpleLimit() throws InterruptedException {
        RateLimitDecorator d = new RateLimitDecorator(3, 0.04);
        java.util.List<Integer> calls = new java.util.ArrayList<>();
        java.util.function.Supplier<Integer> myfun = d.decorate(() -> {
            calls.add(2);
            return calls.stream().mapToInt(Integer::intValue).sum();
        });
        assertEquals(2, (int)myfun.get());
        assertEquals(4, (int)myfun.get());
        assertEquals(6, (int)myfun.get());
        assertThrows(RateLimitException.class, myfun::get);
        Thread.sleep(45);
        assertEquals(8, (int)myfun.get());
    }

    @Test
    void testPublicSleepAndRetry() throws InterruptedException {
        RateLimitDecorator d = new RateLimitDecorator(1, 0.02);
        SleepAndRetry sar = new SleepAndRetry();
        java.util.function.Supplier<Integer> fn = sar.decorate(d.decorate(() -> 24));
        assertEquals(24, (int)fn.get());
        long t0 = System.currentTimeMillis();
        assertEquals(24, (int)fn.get());
        assertTrue((System.currentTimeMillis() - t0) >= 20, "Should sleep at least 20ms");
    }

    @Test
    void testPublicRaiseOnLimitFalse() throws InterruptedException {
        RateLimitDecorator d = new RateLimitDecorator(1, 0.03, false);
        java.util.List<Integer> track = new java.util.ArrayList<>();
        java.util.function.Supplier<Integer> fun = d.decorate(() -> {
            track.add(track.size() + 1);
            return track.get(track.size() - 1);
        });
        assertEquals(1, (int)fun.get());
        assertNull(fun.get());
        Thread.sleep(35);
        assertEquals(2, (int)fun.get());
    }
}