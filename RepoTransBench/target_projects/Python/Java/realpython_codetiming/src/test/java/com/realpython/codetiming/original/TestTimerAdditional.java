package com.realpython.codetiming.original;

import com.realpython.codetiming.Timer;
import com.realpython.codetiming.TimerError;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.ArrayList;
import java.util.List;

public class TestTimerAdditional {
    @Test
    void test_timer_context_manager_runs() throws Exception {
        Timer timer = new Timer("cmmsg", "Elapsed time: {0:.4f}s");
        try (timer) {
            // context entered and exited without error
        }
    }

    @Test
    void test_timer_start_stop_elapsed() {
        Timer timer = new Timer("simple", "Time {0:.4f}");
        assertNull(timer._startTime, "Timer._startTime should initially be null");
        timer.start();
        assertNotNull(timer._startTime, "Timer._startTime should not be null after start");
        timer.stop();
        double elapsed = timer.last;
        assertTrue(elapsed >= 0.0, "Elapsed time should be non-negative");
    }

    @Test
    void test_timer_str_repr() {
        Timer timer = new Timer("simple", "Time {0:.4f}");
        assertTrue(timer.toString() instanceof String);
        assertTrue(timer.toString().contains("Timer"));
    }

    @Test
    void test_timer_running_status_via_private() {
        Timer timer = new Timer("runstat", "Running:{0}");
        timer.start();
        assertNotNull(timer._startTime);
        timer.stop();
        assertNull(timer._startTime);
    }

    @Test
    void test_timer_logger_callable_text() {
        List<String> messages = new ArrayList<>();
        // Using lambda as logger to store calls
        Timer timer = new Timer("cbmsg", null, (msg) -> messages.add("Time=" + msg));
        timer.start();
        timer.stop();
        assertFalse(messages.isEmpty());
        assertTrue(messages.get(0).contains("Time="));
    }

    @Test
    void test_timer_without_text_logger() {
        Timer timer = new Timer("notext", null, null);
        timer.start();
        timer.stop();
        // Should not log or raise
        assertTrue(true);
    }

    @Test
    void test_timer_stop_without_start_raises() {
        Timer timer = new Timer("exception", "fail");
        assertThrows(TimerError.class, timer::stop);
    }

    @Test
    void test_timer_multiple_starts_raises() {
        Timer timer = new Timer("multi", "multi");
        timer.start();
        assertThrows(TimerError.class, timer::start);
        timer.stop();
    }

    @Test
    void test_timer_last_when_nan() {
        Timer timer = new Timer("none", "none");
        assertTrue(Double.isNaN(timer.last));
    }

    @Test
    void test_timer_compare_multiple_instances() {
        Timer timer1 = new Timer("a");
        Timer timer2 = new Timer("b");
        assertNotSame(timer1, timer2);
    }
}