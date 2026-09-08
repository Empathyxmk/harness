package com.trailofbits.protofuzz.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Iterator;
import java.util.HashSet;
import java.util.Set;

public class TestValues {

    public static Iterator<Integer> integralValueGen() {
        // Mimic Python values.integral_value_gen()
        return java.util.Arrays.asList(0, 1, -1, 42, -42, Integer.MAX_VALUE, Integer.MIN_VALUE, 1234).iterator();
    }

    public static Iterator<Float> float32ValueGen() {
        // Mimic Python values.float32_value_gen()
        return java.util.Arrays.asList(0.0f, -1.5f, 1.0f, 3.14159f, Float.NaN, Float.POSITIVE_INFINITY, Float.NEGATIVE_INFINITY, 1.7e+38f).iterator();
    }

    public static Iterator<String> stringValueGen() {
        // Mimic Python values.string_value_gen()
        return java.util.Arrays.asList("", "a", "test", "123", "!", "hello world").iterator();
    }

    @Test
    public void testIntegralValueGen() {
        Iterator<Integer> g = integralValueGen();
        int ct = 0;
        while (g.hasNext() && ct < 8) {
            int v = g.next();
            assertTrue(v == (int) v);
            ct++;
        }
        assertEquals(8, ct);
    }

    @Test
    public void testFloat32ValueGen() {
        Iterator<Float> g = float32ValueGen();
        int ct = 0;
        while (g.hasNext() && ct < 8) {
            float v = g.next();
            assertTrue(v == (float) v);
            ct++;
        }
        assertEquals(8, ct);
    }

    @Test
    public void testStringValueGen() {
        Iterator<String> g = stringValueGen();
        int ct = 0;
        while (g.hasNext() && ct < 6) {
            String v = g.next();
            assertNotNull(v);
            assertTrue(v instanceof String);
            ct++;
        }
        assertEquals(6, ct);
    }
}