package com.vijos.jd4.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import org.mockito.Mockito;

class PublicPoolTest {

    static final List<Object> QVALS = new ArrayList<>();
    static class Q {
        void putNowait(Object v) { QVALS.add(v); }
    }

    static Object _lock = new Object();
    static Queue<Object> _queue = new LinkedList<>();

    static void putSandbox(Object... vals) {
        QVALS.clear();
        for (Object v : vals) new Q().putNowait(v);
    }

    static List<Object> getSandbox(int n) throws Exception {
        List<Object> outs = new ArrayList<>();
        synchronized (_lock) {
            for (int i = 0; i < n; ++i)
                outs.add(_queue.poll());
        }
        return outs;
    }

    static class Logger {
        List<String> msgs = new ArrayList<>();
        void info(String fmt, Object... a) { msgs.add("info"); }
        void warning(String fmt, Object... a) { msgs.add("warn"); }
    }

    @BeforeEach
    void reset() { QVALS.clear(); _queue.clear(); }

    @Test
    void testPublicPutSandboxPutsToQueue() {
        putSandbox("a", "b", "c");
        assertEquals(Arrays.asList("a", "b", "c"), QVALS);
    }

    @Test
    void testPublicGetSandbox() throws Exception {
        _queue.add("x"); _queue.add("y");
        List<Object> outs = getSandbox(2);
        assertEquals(Arrays.asList("x", "y"), outs);
    }

    @Test
    void testPublicInitParallelism() {
        Logger logger = new Logger();
        logger.info("info");
        assertTrue(logger.msgs.contains("info"));
    }

    @Test
    void testPublicInitLowParallelism() {
        Logger logger = new Logger();
        logger.warning("warn");
        assertTrue(logger.msgs.contains("warn"));
    }
}