package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.utils.Utils;

public class UtilsTest {
    @Test
    void testNowReturnsCallableAndReturnsFloat() {
        java.util.function.Supplier<Double> func = Utils.now();
        assertNotNull(func);
        Double value = func.get();
        assertTrue(value instanceof Double);
    }

    @Test
    void testNowFallback() {
        java.util.function.Supplier<Double> fn = Utils.now(); // fallback not possible to simulate as in Python
        assertNotNull(fn);
        double diff = Math.abs(fn.get() - System.currentTimeMillis()/1000.0);
        assertTrue(diff < 1.0);
    }
}