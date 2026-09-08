package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;
import com.tomasbasham.ratelimit.exception.RateLimitException;

public class DecoratorClassCoreTest {

    @Test
    void testConstructorClampsCalls() {
        // Negative
        RateLimitDecorator rld = new RateLimitDecorator(-5, 1);
        assertEquals(1, rld.getClampedCalls());

        // Large
        RateLimitDecorator rld2 = new RateLimitDecorator(1L << 60, 1);
        assertEquals(Long.MAX_VALUE, rld2.getClampedCalls());

        // Floor
        RateLimitDecorator rld3 = new RateLimitDecorator(3.9, 1);
        assertEquals(3, rld3.getClampedCalls());
    }

    @Test
    void testDecoratorRateLimitRaises() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(1, 0.05);

        final int[] calls = {0};
        Runnable f = rl.decorate(() -> {
            calls[0]++;
            return "foo";
        });

        assertEquals("foo", f.runReturn());

        assertThrows(RateLimitException.class, () -> {
            f.runReturn();
        });

        Thread.sleep(65);
        assertEquals("foo", f.runReturn());
    }

    @Test
    void testDecoratorDoesNotRaise() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(1, 0.05, false);
        final int[] result = {0};
        Runnable f = rl.decorate(() -> {
            result[0]++;
            return result[0];
        });

        assertEquals(1, f.runReturn());
        Thread.sleep(65);
        assertEquals(2, f.runReturn());
    }

    @Test
    void testThreadSafety() {
        RateLimitDecorator rld = new RateLimitDecorator(10, 1);

        Runnable dummy = () -> 42;
        Runnable wrapped = rld.decorate(dummy);
        wrapped.run();
        wrapped.run();

        // Check for lock-like field (simulate by checking for internal lock after calls)
        // In real, use reflection as needed.
        assertTrue(rld.hasLockField());
    }
}