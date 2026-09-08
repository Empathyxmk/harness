package com.ecmwf.ai_models.original;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Path;
import java.util.logging.*;
import com.ecmwf.ai_models.stepper.Stepper;

class StepperTest {
    static class LogHandler extends Handler {
        private final StringBuilder sb = new StringBuilder();
        @Override public void publish(LogRecord record) { sb.append(record.getMessage()).append("\n"); }
        @Override public void flush() {}
        @Override public void close() throws SecurityException {}
        public String getText() { return sb.toString(); }
    }

    @Test
    void test_stepper_basic() throws IOException {
        LogHandler handler = new LogHandler();
        Logger logger = Logger.getLogger(Stepper.class.getName());
        logger.addHandler(handler);
        logger.setUseParentHandlers(false);
        Stepper s = new Stepper(2, 6);
        Assertions.assertEquals(3, s.numSteps);
        s.start();
        s.call(0, 2);
        s.call(1, 2);
        s.call(2, 2);
        s.close(); // triggers logging
        String logs = handler.getText();
        Assertions.assertTrue(logs.contains("Elapsed"));
        Assertions.assertTrue(logs.contains("Average"));
        logger.removeHandler(handler);
    }

    @Test
    void test_stepper_zero_steps() throws IOException {
        LogHandler handler = new LogHandler();
        Logger logger = Logger.getLogger(Stepper.class.getName());
        logger.addHandler(handler);
        logger.setUseParentHandlers(false);
        Stepper s = new Stepper(5, 0);
        s.start();
        s.close();  // Should not log Average
        String logs = handler.getText();
        Assertions.assertTrue(logs.contains("Elapsed"));
        Assertions.assertFalse(logs.contains("Average"));
        logger.removeHandler(handler);
    }
}