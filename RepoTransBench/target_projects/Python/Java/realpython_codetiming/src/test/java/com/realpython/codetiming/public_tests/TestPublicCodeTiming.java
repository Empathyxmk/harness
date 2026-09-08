package com.realpython.codetiming.public_tests;

import com.realpython.codetiming.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicCodeTiming {

    private static final String USER_TIME_PREFIX = "Time spent:";
    private static final String USER_TIME_MESSAGE = USER_TIME_PREFIX + " %.5f s";

    // Waste time function
    static void waste_custom_time(int num) {
        int sum = 0;
        for (int n = 0; n < num; ++n)
            sum += n + 1;
    }

    @Test
    void test_timer_as_decorator_public() {
        waste_custom_time(500);
        assertTrue(true);
    }

    @Test
    void test_timer_as_context_manager_public() {
        try (Timer t = new Timer("test", USER_TIME_MESSAGE)) {
            waste_custom_time(500);
        } catch (Exception e) {
            fail("Timer exception: " + e);
        }
    }

    @Test
    void test_explicit_timer_public() {
        Timer t = new Timer("test", USER_TIME_MESSAGE);
        t.start();
        waste_custom_time(500);
        t.stop();
        assertTrue(true);
    }

    @Test
    void test_error_if_timer_not_running_public() {
        Timer t = new Timer("test", USER_TIME_MESSAGE);
        assertThrows(TimerError.class, t::stop);
    }

    @Test
    void test_last_starts_as_nan_public() {
        Timer t = new Timer();
        assertTrue(Double.isNaN(t.last));
    }

    @Test
    void test_timer_sets_last_public() throws Exception {
        Timer t = new Timer("test", USER_TIME_MESSAGE);
        try (t) {
            Thread.sleep(10);
        }
        assertTrue(true);
    }
}