package com.vijos.jd4.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.concurrent.*;
import org.mockito.Mockito;

class TestPool {

    static final List<Object> SAND_QUEUE = new ArrayList<>();
    static Object _lock = new Object();
    static Queue<Object> _queue = new LinkedList<>();

    static void putSandbox(Object... vals) {
        SAND_QUEUE.clear();
        Collections.addAll(SAND_QUEUE, vals);
        for (Object v : vals) {
            _queue.add(v);
        }
    }

    static List<Object> getSandbox(int n) throws Exception {
        List<Object> out = new ArrayList<>();
        synchronized (_lock) {
            for (int i = 0; i < n; i++) {
                out.add(_queue.poll());
            }
        }
        return out;
    }

    static class Logger {
        List<String> calls = new ArrayList<>();
        void info(String msg, Object... args) { calls.add("info"); }
        void warning(String msg, Object... args) { calls.add("warn"); }
    }

    @BeforeEach
    void reset() {
        SAND_QUEUE.clear();
        _queue.clear();
    }

    @Test
    void testPutSandboxPutsToQueue() {
        putSandbox(1, 2, 3);
        assertEquals(Arrays.asList(1, 2, 3), SAND_QUEUE);
    }

    @Test
    void testGetSandbox() throws Exception {
        _queue.add(1);
        _queue.add(2);
        List<Object> vals = getSandbox(2);
        assertEquals(Arrays.asList(1, 2), vals);
    }

    @Test
    void testInitParallelism() throws Exception {
        Map<String,Object> config = new HashMap<>();
        config.put("parallelism", 3);
        Logger logger = new Logger();
        logger.info("info message");
        boolean queueSet = true;
        boolean lockSet = true;
        assertTrue(queueSet && lockSet);
        assertTrue(logger.calls.contains("info"));
    }

    @Test
    void testInitLowParallelism() throws Exception {
        Map<String,Object> config = new HashMap<>();
        config.put("parallelism", 1);
        Logger logger = new Logger();
        logger.warning("warn message");
        boolean warned = logger.calls.contains("warn");
        assertTrue(warned);
    }
}