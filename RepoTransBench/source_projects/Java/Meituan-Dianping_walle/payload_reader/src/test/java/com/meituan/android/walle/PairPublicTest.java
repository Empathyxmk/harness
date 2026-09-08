package com.meituan.android.walle;

import org.junit.Test;

import static org.junit.Assert.*;

public class PairPublicTest {

    @Test
    public void testOfAndGetters_public() {
        Pair<Integer, String> pair = Pair.of(12345, "hello");
        assertEquals(Integer.valueOf(12345), pair.getFirst());
        assertEquals("hello", pair.getSecond());

        Pair<Double, Double> pair2 = Pair.of(3.14, 2.71);
        assertEquals(Double.valueOf(3.14), pair2.getFirst());
        assertEquals(Double.valueOf(2.71), pair2.getSecond());
    }

    @Test
    public void testEqualsAndHashCode_public() {
        Pair<String, String> a = Pair.of("A", "B");
        Pair<String, String> b = Pair.of("A", "B");
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());

        Pair<String, String> c = Pair.of("A", "C");
        assertNotEquals(a, c);

        Pair<String, String> d = Pair.of(null, "B");
        Pair<String, String> e = Pair.of(null, "B");
        assertEquals(d, e);
        assertEquals(d.hashCode(), e.hashCode());
    }
}