package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;
import com.tomasbasham.ratelimit.exception.RateLimitException;

public class PublicDecoratorClassCoreTest {

    @Test
    void testPublicConstructorClampsCalls() {
        RateLimitDecorator rld = new RateLimitDecorator(0, 2);
        assertEquals(1, rld.getClampedCalls());

        RateLimitDecorator rld2 = new RateLimitDecorator(Long.MAX_VALUE + 100L, 2);
        assertEquals(Long.MAX_VALUE, rld2.getClampedCalls());

        RateLimitDecorator rld3 = new RateLimitDecorator(7.8, 2);
        assertEquals(7, rld3.getClampedCalls());
    }

    @Test
    void testPublicDecoratorRateLimitRaises() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(2, 0.03);
        final int[] calls = {0};

        java.util.function.Supplier<String> foo = rl.decorate(() -> "bar");
        assertEquals("bar", foo.get());
        assertEquals("bar", foo.get());
        assertThrows(RateLimitException.class, foo::get);
        Thread.sleep(40);
        assertEquals("bar", foo.get());
    }

    @Test
    void testPublicDecoratorDoesNotRaise() throws InterruptedException {
        RateLimitDecorator rl = new RateLimitDecorator(2, 0.04, false);
        java.util.List<String> result = new java.util.ArrayList<>();
        java.util.function.Supplier<Integer> bar = rl.decorate(() -> {
            result.add("x");
            return result.size();
        });
        assertEquals(1, (int)bar.get());
        assertEquals(2, (int)bar.get());
        Thread.sleep(45);
        assertEquals(3, (int)bar.get());
    }

    @Test
    void testPublicThreadSafety() {
        // Thread safety test is tricky, so we call multiple times and look for lock
        RateLimitDecorator rld = new RateLimitDecorator(4, 1);
        java.util.function.Supplier<Integer> dummy2 = rld.decorate(() -> 24);
        dummy2.get();
        dummy2.get();
        dummy2.get();
        assertTrue(rld.hasLockField());
    }
}