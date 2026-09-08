package com.realpython.codetiming.public_tests;

import com.realpython.codetiming.Timer;
import com.realpython.codetiming.TimerError;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.ArrayList;
import java.util.List;

public class TestPublicTimerAdditional {
    @Test
    void test_timer_context_manager_runs_public() throws Exception {
        Timer timer = new Timer("public_cmmsg", "Public elapsed: {0:.6f}s");
        try (timer) {
            int x = 42;
            assertEquals(42, x); // confirm code in context
        }
    }

    @Test
    void test_timer_start_stop_elapsed_public() {
        Timer timer = new Timer("public_simple", "Duration {0:.2f}");
        assertNull(timer._startTime);
        timer.start();
        assertNotNull(timer._startTime);
        timer.stop();
        double elapsed = timer.last;
        assertTrue(elapsed >= 0.0);
    }

    @Test
    void test_timer_str_repr_public() {
        Timer timer = new Timer("public_simple", "Duration {0:.2f}");
        assertTrue(timer.toString() instanceof String);
        assertTrue(timer.toString().contains("Timer"));
    }

    @Test
    void test_timer_running_status_via_private_public() {
        Timer timer = new Timer("public_runstat", "Now running:{0}");
        timer.start();
        assertNotNull(timer._startTime);
        timer.stop();
        assertNull(timer._startTime);
    }

    @Test
    void test_timer_logger_callable_text_public() {
        List<String> messages = new ArrayList<>();
        Timer timer = new Timer("public_cbmsg", null, (msg) -> messages.add("Elapsed=" + msg));
        timer.start();
        timer.stop();
        assertFalse(messages.isEmpty());
        assertTrue(messages.get(0).contains("Elapsed="));
    }

    @Test
    void test_timer_without_text_logger_public() {
        Timer timer = new Timer("public_notext", null, null);
        timer.start();
        timer.stop();
        assertTrue(true);
    }

    @Test
    void test_timer_stop_without_start_raises_public() {
        Timer timer = new Timer("public_exception", "fail fast");
        assertThrows(TimerError.class, timer::stop);
    }

    @Test
    void test_timer_multiple_starts_raises_public() {
        Timer timer = new Timer("public_multi", "multi-case");
        timer.start();
        assertThrows(TimerError.class, timer::start);
        timer.stop();
    }

    @Test
    void test_timer_last_when_nan_public() {
        Timer timer = new Timer("public_none", "noneCase");
        assertTrue(Double.isNaN(timer.last));
    }

    @Test
    void test_timer_compare_multiple_instances_public() {
        Timer timer1 = new Timer("public_x");
        Timer timer2 = new Timer("public_y");
        assertNotSame(timer1, timer2);
    }
}