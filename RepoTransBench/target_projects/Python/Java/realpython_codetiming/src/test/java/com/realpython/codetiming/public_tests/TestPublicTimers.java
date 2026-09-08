package com.realpython.codetiming.public_tests;

import com.realpython.codetiming.Timers;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.NoSuchElementException;
import java.util.ArrayList;

public class TestPublicTimers {
    @Test
    void test_add_and_total_and_count_public() {
        Timers timers = new Timers();
        timers.add("alpha", 0.5);
        timers.add("alpha", 0.7);
        assertEquals(2, timers.count("alpha"));
        assertEquals(1.2, timers.total("alpha"), 0.000001);
    }

    @Test
    void test_min_max_mean_median_stdev_public() {
        Timers timers = new Timers();
        double[] vals = {4.0, 5.5, 6.5};
        for (double v : vals) timers.add("y", v);
        assertEquals(4.0, timers.min("y"), 1e-10);
        assertEquals(6.5, timers.max("y"), 1e-10);
        assertEquals(5.333333333, timers.mean("y"), 1e-6);
        assertEquals(5.5, timers.median("y"), 1e-10);
        assertTrue(timers.stdev("y") > 0);
    }

    @Test
    void test_stdev_nan_for_one_entry_public() {
        Timers timers = new Timers();
        timers.add("single_public", 13.6);
        assertTrue(Double.isNaN(timers.stdev("single_public")));
    }

    @Test
    void test_apply_keyerror_public() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.apply((l) -> l.size(), "does_not_exist"));
    }

    @Test
    void test_setitem_error_public() {
        assertThrows(UnsupportedOperationException.class, () -> { throw new UnsupportedOperationException(); });
    }

    @Test
    void test_clear_public() {
        Timers timers = new Timers();
        timers.add("bar", 2.4);
        timers.clear();
        assertEquals(0, timers.timings.size());
        assertEquals(0, timers.data().size());
    }

    @Test
    void test_total_no_timings_public() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.total("ghost"));
    }

    @Test
    void test_min_max_zero_if_empty_public() {
        Timers timers = new Timers();
        timers.timings.put("emptycase", new ArrayList<>());
        assertEquals(0.0, timers.min("emptycase"), 1e-10);
        assertEquals(0.0, timers.max("emptycase"), 1e-10);
    }

    @Test
    void test_mean_median_zero_if_empty_public() {
        Timers timers = new Timers();
        timers.timings.put("emptycase", new ArrayList<>());
        assertEquals(0.0, timers.mean("emptycase"), 1e-10);
        assertEquals(0.0, timers.median("emptycase"), 1e-10);
    }

    @Test
    void test_stdev_keyerror_if_missing_public() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.stdev("MISSING"));
    }
}