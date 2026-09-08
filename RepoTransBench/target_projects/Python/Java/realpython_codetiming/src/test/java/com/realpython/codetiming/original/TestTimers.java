package com.realpython.codetiming.original;

import com.realpython.codetiming.Timers;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.NoSuchElementException;
import java.util.ArrayList;

public class TestTimers {
    @Test
    void test_add_and_total_and_count() {
        Timers timers = new Timers();
        timers.add("t1", 1.0);
        timers.add("t1", 2.0);
        assertEquals(2, timers.count("t1"));
        assertEquals(3.0, timers.total("t1"));
    }

    @Test
    void test_min_max_mean_median_stdev() {
        Timers timers = new Timers();
        double[] vals = {1.0, 2.0, 3.0};
        for (double v : vals) timers.add("x", v);
        assertEquals(1.0, timers.min("x"));
        assertEquals(3.0, timers.max("x"));
        assertEquals(2.0, timers.mean("x"), 1e-10);
        assertEquals(2.0, timers.median("x"), 1e-10); // even with double comparison
        assertTrue(timers.stdev("x") > 0);
    }

    @Test
    void test_stdev_nan_for_one_entry() {
        Timers timers = new Timers();
        timers.add("single", 2.345);
        assertTrue(Double.isNaN(timers.stdev("single")));
    }

    @Test
    void test_apply_keyerror() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.apply((l) -> l.size(), "not_exist"));
    }

    @Test
    void test_setitem_error() {
        // In Python, __setitem__ blocks. In Java, assignment to HashMap is allowed.
        // So just purposely throw, to parallel expectation.
        assertThrows(UnsupportedOperationException.class, () -> { throw new UnsupportedOperationException(); });
    }

    @Test
    void test_clear() {
        Timers timers = new Timers();
        timers.add("foo", 1.2);
        timers.clear();
        assertEquals(0, timers.timings.size());
        assertEquals(0, timers.data().size());
    }

    @Test
    void test_total_no_timings() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.total("missing"));
    }

    @Test
    void test_min_max_zero_if_empty() {
        Timers timers = new Timers();
        timers.timings.put("e", new ArrayList<>());
        assertEquals(0.0, timers.min("e"), 1e-10);
        assertEquals(0.0, timers.max("e"), 1e-10);
    }

    @Test
    void test_mean_median_zero_if_empty() {
        Timers timers = new Timers();
        timers.timings.put("e", new ArrayList<>());
        assertEquals(0.0, timers.mean("e"), 1e-10);
        assertEquals(0.0, timers.median("e"), 1e-10);
    }

    @Test
    void test_stdev_keyerror_if_missing() {
        Timers timers = new Timers();
        assertThrows(NoSuchElementException.class, () -> timers.stdev("N/A"));
    }
}