package com.facebook.sparts.public_;

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

public class PublicCountersTest {
    @Test
    public void testPublicSum() {
        MockCounter c = new MockCounter();
        assertEquals(0.0, c.call(), 0.000001);
        c.incrementBy(3);
        assertEquals(3.0, c.call(), 0.000001);
        c.increment();
        assertEquals(4.0, c.call(), 0.000001);
        c.add(6);
        assertEquals(10.0, c.call(), 0.000001);

        assertEquals(10, (int)c.call());
        assertEquals(10.0, (float)c.call(), 0.000001);
        assertEquals("10.0", c.toString());

        c.reset(5.5);
        assertEquals(5.5, c.call(), 0.000001);
    }

    @Test
    public void testPublicCount() {
        CounterCount c = new CounterCount();
        assertEquals(0, c.call());
        c.add(55);
        assertEquals(1, c.call());
    }

    @Test
    public void testPublicMax() {
        CounterMax c = new CounterMax();
        assertNull(c.call());
        c.add(5);
        assertEquals(5.0, c.call(), 0.000001);
        c.add(-15);
        assertEquals(5.0, c.call(), 0.000001);
        c.add(15);
        assertEquals(15.0, c.call(), 0.000001);
    }

    @Test
    public void testPublicMin() {
        CounterMin c = new CounterMin();
        assertNull(c.call());
        c.add(5);
        assertEquals(5.0, c.call(), 0.000001);
        c.add(-15);
        assertEquals(-15.0, c.call(), 0.000001);
        c.add(2);
        assertEquals(-15.0, c.call(), 0.000001);
    }

    @Test
    public void testPublicAverage() {
        CounterAverage c = new CounterAverage();
        assertNull(c.call());
        c.add(20);
        c.add(40);
        assertEquals(30.0, c.call(), 0.000001);
    }

    @Test
    public void testPublicCallbackCounter() {
        final double[] l = {42.0};
        CallbackCounter c = new CallbackCounter(() -> l[0]);
        assertEquals(42.0, c.call(), 0.000001);
        l[0] = 7.0;
        assertEquals(7.0, c.call(), 0.000001);
    }
}