package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.utils.Utils;

public class UtilsAdditionalTest {
    @Test
    void testNowReturnsMonotonicOrTime() throws InterruptedException {
        // Assume Utils.now() returns a supplier of time in double
        java.util.function.Supplier<Double> func = Utils.now();
        assertNotNull(func);
        double t1 = func.get();
        Thread.sleep(10);
        double t2 = func.get();
        assertTrue(t2 > t1);

        // No monkeypatch for time.monotonic in Java, so this fallback is not directly needed
    }
}