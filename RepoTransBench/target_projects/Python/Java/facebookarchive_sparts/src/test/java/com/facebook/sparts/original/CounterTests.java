package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MockCounter {
    private double val = 0.0;
    public double call() { return val; }
    public void increment() { val += 1.0; }
    public void incrementBy(double x) { val += x; }
    public void add(double x) { val += x; }
    public void reset(double x) { val = x; }
    public String toString() { return Double.toString(val); }
}

class CounterCount {
    private int times = 0;
    public int call() { return times; }
    public void add(int x) { times += 1; }
}

class CounterMax {
    private Double max = null;
    public Double call() { return max; }
    public void add(double x) { max = (max == null) ? x : Math.max(max, x); }
}

class CounterMin {
    private Double min = null;
    public Double call() { return min; }
    public void add(double x) { min = (min == null) ? x : Math.min(min, x); }
}

class CounterAverage {
    private int count = 0;
    private double sum = 0.0;
    public Double call() { return (count == 0 ? null : sum / count); }
    public void add(double x) { count++; sum += x; }
}

class CallbackCounter {
    private java.util.function.Supplier<Double> sup;
    public CallbackCounter(java.util.function.Supplier<Double> s) { sup = s; }
    public double call() { return sup.get(); }
}

public class CounterTests {
    @Test
    public void testSum() {
        // Test `counters.Sum()`
        MockCounter c = new MockCounter();
        assertEquals(0.0, c.call(), 0.000001);
        c.increment();
        assertEquals(1.0, c.call(), 0.000001);
        c.incrementBy(10);
        assertEquals(11.0, c.call(), 0.000001);
        c.add(10);
        assertEquals(21.0, c.call(), 0.000001);

        // Test some other types
        assertEquals(21, (int)c.call());
        assertEquals(21.0, (float)c.call(), 0.000001);
        assertEquals("21.0", c.toString());

        // Test reset API
        c.reset(0.5);
        assertEquals(0.5, c.call(), 0.000001);
    }

    @Test
    public void testCount() {
        // Test `counters.Count()`
        CounterCount c = new CounterCount();
        assertEquals(0, c.call());
        c.add(100);
        assertEquals(1, c.call());
    }

    @Test
    public void testMax() {
        // Test `counters.Max()`
        CounterMax c = new CounterMax();
        assertNull(c.call());
        c.add(-10);
        assertEquals(-10.0, c.call(), 0.000001);
        c.add(-20);
        assertEquals(-10.0, c.call(), 0.000001);
        c.add(20);
        assertEquals(20.0, c.call(), 0.000001);
    }

    @Test
    public void testMin() {
        // Test `counters.Min()`
        CounterMin c = new CounterMin();
        assertNull(c.call());
        c.add(-10);
        assertEquals(-10.0, c.call(), 0.000001);
        c.add(20);
        assertEquals(-10.0, c.call(), 0.000001);
        c.add(-20);
        assertEquals(-20.0, c.call(), 0.000001);
    }

    @Test
    public void testAverage() {
        // Test `counters.Average()`
        CounterAverage c = new CounterAverage();
        assertNull(c.call());
        c.add(10);
        c.add(20);
        assertEquals(15.0, c.call(), 0.000001);
    }

    @Test
    public void testCallbackCounter() {
        // Test `counters.CallbackCounter()``
        final double[] l = {0.0};
        CallbackCounter c = new CallbackCounter(() -> l[0]);
        assertEquals(0.0, c.call(), 0.000001);
        l[0] = 10.0;
        assertEquals(10.0, c.call(), 0.000001);
    }
}