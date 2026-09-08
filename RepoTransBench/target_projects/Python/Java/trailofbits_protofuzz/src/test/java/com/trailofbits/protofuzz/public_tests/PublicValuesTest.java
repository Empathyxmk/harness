package com.trailofbits.protofuzz.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class PublicValuesTest {
    public static Iterator<Integer> integralValueGen() {
        return java.util.Arrays.asList(0, 1, -1, 2, -2, 42, -42, 100, -100).iterator();
    }

    public static Iterator<Float> float32ValueGen() {
        return java.util.Arrays.asList(-1.23f, 0.0f, 1.23f, 3.1415f, 2.71f, -2.71f, 100.0f, -100.0f, Float.POSITIVE_INFINITY, Float.NEGATIVE_INFINITY).iterator();
    }

    public static Iterator<String> stringValueGen() {
        return java.util.Arrays.asList("", "foo", "bar", "baz", "longstring", "abc", "def", "xyz!@#", " ").iterator();
    }

    @Test
    public void testIntegralValueGenPublic() {
        List<Integer> vals = new ArrayList<>();
        Iterator<Integer> g = integralValueGen();
        while (g.hasNext()) vals.add(g.next());
        assertFalse(vals.isEmpty());
        for (int v : vals) assertTrue(v == (int)v);
        Set<Integer> uniq = new HashSet<>(vals);
        assertEquals(uniq.size(), vals.size());
        boolean hasNeg = false, hasPos = false;
        for (int v : vals) {
            if (v < 0) hasNeg = true;
            if (v >= 0) hasPos = true;
        }
        assertTrue(hasNeg && hasPos);
        assertTrue(vals.size() > 5);
    }

    @Test
    public void testFloat32ValueGenPublic() {
        List<Float> vals = new ArrayList<>();
        Iterator<Float> g = float32ValueGen();
        while (g.hasNext()) vals.add(g.next());
        assertFalse(vals.isEmpty());
        for (float v : vals) assertTrue(v == (float)v);
        Set<Float> uniq = new HashSet<>(vals);
        assertEquals(uniq.size(), vals.size());
        boolean lessOne = false, moreOne = false;
        for (float v : vals) {
            if (Math.abs(v) < 1.0) lessOne = true;
            if (Math.abs(v) > 1.0 && !Float.isInfinite(v)) moreOne = true;
        }
        assertTrue(lessOne);
        assertTrue(moreOne);
        assertTrue(vals.size() > 7);
    }

    @Test
    public void testStringValueGenPublic() {
        List<String> vals = new ArrayList<>();
        Iterator<String> g = stringValueGen();
        while (g.hasNext()) vals.add(g.next());
        assertFalse(vals.isEmpty());
        for (String v : vals) assertTrue(v instanceof String);
        Set<String> uniq = new HashSet<>(vals);
        assertEquals(uniq.size(), vals.size());
        boolean hasLong = false;
        for (String v : vals) {
            if (v.length() > 3) hasLong = true;
        }
        assertTrue(hasLong);
        assertTrue(vals.size() > 5);
    }
}