package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;

public class DecoratorsEdgeCasesTest {

    @Test
    void testClampedCallsMinAndMax() {
        RateLimitDecorator d = new RateLimitDecorator(-9, 1);
        assertEquals(1, d.getClampedCalls());

        RateLimitDecorator d2 = new RateLimitDecorator(Long.MAX_VALUE + 123456.0, 1);
        assertEquals(Long.MAX_VALUE, d2.getClampedCalls());
    }

    @Test
    void testDecoratorThreadSafety() throws InterruptedException {
        java.util.List<Integer> result = java.util.Collections.synchronizedList(new java.util.ArrayList<>());
        RateLimitDecorator dec = new RateLimitDecorator(2, 1);
        java.util.function.Function<Integer, Integer> foo = dec.decorate((Integer x) -> {
            result.add(x);
            return x;
        });

        Thread t1 = new Thread(() -> foo.apply(1));
        Thread t2 = new Thread(() -> foo.apply(2));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        java.util.Collections.sort(result);
        assertEquals(java.util.Arrays.asList(1, 2), result);
    }

    @Test
    void testPeriodRemainingZero() {
        // Simulate by manual control of clock and reset.
        final int[] state = {10};
        RateLimitDecorator dec = new RateLimitDecorator(2, 5);
        dec.setLastReset(15);
        dec.setClock(() -> 20.0);
        java.util.List<String> called = new java.util.ArrayList<>();
        java.util.function.Supplier<Integer> f = dec.decorate(() -> {
            called.add("called");
            return 123;
        });
        assertEquals(123, (int)f.get());
        assertEquals(123, (int)f.get());
    }

    @Test
    void testPeriodRemainingNegative() {
        final int[] t = {0};
        RateLimitDecorator dec = new RateLimitDecorator(1, 1);
        dec.setClock(() -> {
            int val = t[0];
            t[0] += 100;
            return (double) val;
        });
        java.util.List<Integer> called = new java.util.ArrayList<>();
        java.util.function.Supplier<Void> foo = dec.decorate(() -> {
            called.add(1);
            return null;
        });
        foo.get();
        foo.get();
        assertEquals(2, called.size());
    }
}