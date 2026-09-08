package com.meituan.android.walle;

import org.junit.Test;
import static org.junit.Assert.*;

public class PairTest {

    @Test
    public void testOfGetters() {
        Pair<String, Integer> pair = Pair.of("hello", 42);
        assertEquals("hello", pair.getFirst());
        assertEquals(Integer.valueOf(42), pair.getSecond());
    }

    @Test
    public void testEqualsHashCode_sameObject() {
        Pair<String, Integer> pair = Pair.of("foo", 123);
        assertTrue(pair.equals(pair));
        assertEquals(pair.hashCode(), pair.hashCode());
    }

    @Test
    public void testEqualsHashCode_equalPairs() {
        Pair<String, Integer> pair1 = Pair.of("a", 1);
        Pair<String, Integer> pair2 = Pair.of("a", 1);
        assertTrue(pair1.equals(pair2));
        assertTrue(pair2.equals(pair1));
        assertEquals(pair1.hashCode(), pair2.hashCode());
    }

    @Test
    public void testEquals_notEqualByFirst() {
        Pair<String, Integer> pair1 = Pair.of("a", 1);
        Pair<String, Integer> pair2 = Pair.of("b", 1);
        assertFalse(pair1.equals(pair2));
        assertFalse(pair2.equals(pair1));
    }

    @Test
    public void testEquals_notEqualBySecond() {
        Pair<String, Integer> pair1 = Pair.of("a", 1);
        Pair<String, Integer> pair2 = Pair.of("a", 2);
        assertFalse(pair1.equals(pair2));
        assertFalse(pair2.equals(pair1));
    }

    @Test
    public void testEquals_nullObject() {
        Pair<String, Integer> pair = Pair.of("x", 10);
        assertFalse(pair.equals(null));
    }

    @Test
    public void testEquals_differentClass() {
        Pair<String, Integer> pair = Pair.of("x", 10);
        assertFalse(pair.equals("not a pair"));
    }

    @Test
    public void testEquals_nullFields() {
        Pair<String, Integer> p1 = Pair.of(null, null);
        Pair<String, Integer> p2 = Pair.of(null, null);
        assertTrue(p1.equals(p2));
        assertEquals(p1.hashCode(), p2.hashCode());
    }

    @Test
    public void testEquals_nullFirstDifferentSecond() {
        Pair<String, Integer> p1 = Pair.of(null, 10);
        Pair<String, Integer> p2 = Pair.of(null, 11);
        assertFalse(p1.equals(p2));
    }

    @Test
    public void testEquals_differentFirstNullSecond() {
        Pair<String, Integer> p1 = Pair.of("x", null);
        Pair<String, Integer> p2 = Pair.of("y", null);
        assertFalse(p1.equals(p2));
    }

    @Test
    public void testEquals_nullFirstNonNullOther() {
        Pair<String, Integer> p1 = Pair.of(null, 1);
        Pair<String, Integer> p2 = Pair.of("z", 1);
        assertFalse(p1.equals(p2));
    }

    @Test
    public void testEquals_nonNullFirstNullOther() {
        Pair<String, Integer> p1 = Pair.of("z", 1);
        Pair<String, Integer> p2 = Pair.of(null, 1);
        assertFalse(p1.equals(p2));
    }
}