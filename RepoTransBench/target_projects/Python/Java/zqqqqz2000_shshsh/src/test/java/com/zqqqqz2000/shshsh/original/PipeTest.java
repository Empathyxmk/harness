package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

import static org.junit.jupiter.api.Assertions.*;

class PipeTest {
    static class DummyPipe {
        boolean closed = false;
        void close() { closed = true; }
        boolean isClosed() { return closed; }
    }

    static class PipeGroup {
        DummyPipe[] pipes;
        PipeGroup(int n) {
            pipes = new DummyPipe[n];
            for (int i = 0; i < n; i++) pipes[i] = new DummyPipe();
        }
        void closeAll() {
            for (DummyPipe pipe : pipes) pipe.close();
        }
    }

    PipeGroup pg;

    @BeforeEach
    void setup() {
        pg = new PipeGroup(3);
    }

    @Test
    void testPipeCreation() {
        assertEquals(3, pg.pipes.length);
        for (DummyPipe pipe : pg.pipes) {
            assertNotNull(pipe);
            assertFalse(pipe.isClosed());
        }
    }

    @Test
    void testPipeGroupClose() {
        pg.closeAll();
        for (DummyPipe pipe : pg.pipes) {
            assertTrue(pipe.isClosed());
        }
    }
}