package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.limits;
import com.tomasbasham.ratelimit.RateLimitException;

public class DecoratorTest {

    private int count;

    @BeforeEach
    public void setUp() {
        count = 0;
        // clock.increment(10);
    }

    @Test
    void testIncrement() {
        limits l = new limits(1, 10); // simulate clock in Java
        Runnable increment = l.decorate(() -> count++);
        increment.run();
        assertEquals(1, count);
    }

    @Test
    void testException() {
        limits l = new limits(1, 10); // simulate clock in Java
        Runnable increment = l.decorate(() -> count++);
        increment.run();
        assertThrows(RateLimitException.class, increment::run);
    }

    @Test
    void testReset() {
        limits l = new limits(1, 10); // simulate clock in Java
        Runnable increment = l.decorate(() -> count++);
        increment.run();
        // clock.increment(10); // simulate time advance
        increment.run();
        assertEquals(2, count);
    }

    @Test
    void testNoException() {
        limits l = new limits(1, 10, false); // raise_on_limit false
        Runnable incrementNoException = l.decorate(() -> count++);
        incrementNoException.run();
        incrementNoException.run();
        assertEquals(1, count);
    }
}