package com.trailofbits.protofuzz.original;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class TestLog {

    static class Logger {
        boolean debug = false;
        StringBuilder output = new StringBuilder();

        void setLevelDebug(boolean level) {
            debug = level;
        }

        void debug(String msg) {
            if (debug) output.append(msg).append('\n');
        }

        String getOutput() {
            return output.toString();
        }
        void clear() {
            output.setLength(0);
        }
    }

    Logger logger;

    @BeforeEach
    void setup() {
        logger = new Logger();
    }

    @Test
    public void testLogDebugAndSetlevel() {
        logger.setLevelDebug(true);
        logger.debug("test debug msg");
        String output = logger.getOutput();
        assertTrue(output.contains("test debug msg"));
    }

    @Test
    public void testLogDisableDebug() {
        logger.setLevelDebug(false);
        logger.debug("noapi");
        String output = logger.getOutput();
        assertFalse(output.contains("noapi"));
    }
}